import lucene
import os
import sys
import sqlite3
import threading
import time
from datetime import datetime
import jieba
from urllib.parse import urlparse

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    webpage_index_store_dir = 'index/webpages/'
    image_index_store_dir = 'index/images/'
    if not os.path.exists(webpage_index_store_dir):
        os.mkdir(webpage_index_store_dir)
    if not os.path.exists(image_index_store_dir):
        os.mkdir(image_index_store_dir)

    # create a webpage index writer
    store = SimpleFSDirectory(File(webpage_index_store_dir).toPath())
    analyzer = WhitespaceAnalyzer()
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    webpage_writer = IndexWriter(store, config)

    # create an image index writer
    # DON'T share IndexWriterConfig instances across IndexWriters.
    # make a copy here
    store = SimpleFSDirectory(File(image_index_store_dir).toPath())
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    image_writer = IndexWriter(store, config)

    # add documents to the index
    # the field type for filename and URL
    unindexed_stored_fieldtype = FieldType()
    unindexed_stored_fieldtype.setStored(True)
    unindexed_stored_fieldtype.setTokenized(False)

    content_fieldtype = FieldType()
    content_fieldtype.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    # the field type for title
    # Titles should not only be indexed and tokenized, but also stored to be
    # returned as search results.
    stored_text_fieldtype = FieldType(content_fieldtype)
    stored_text_fieldtype.setStored(True)

    # the field type for sites
    site_fieldtype = FieldType()
    site_fieldtype.setStored(True)
    site_fieldtype.setTokenized(False)
    site_fieldtype.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    # index webpages
    webpage_db = sqlite3.connect('crawled/webpage_list.sqlite')
    cursor = webpage_db.cursor()
    table_name = cursor.execute(
        'SELECT name FROM sqlite_master '
        'WHERE type=\'table\' ORDER BY name DESC LIMIT 1'
    ).fetchone()[0]
    for row in cursor.execute('SELECT * FROM ' + table_name):
        url, title, filename = row
        print('Adding ' + filename)
        doc = Document()

        with open('crawled/text/' + filename, 'r') as f:
            try:
                # use jieba to cut texts into words
                content = ' '.join(jieba.cut_for_search(f.read()))
            except UnicodeDecodeError:
                continue            # skip decoding errors
            doc.add(Field('content', content, content_fieldtype))
        doc.add(Field('filename', filename, unindexed_stored_fieldtype))
        doc.add(Field('title', ' '.join(jieba.cut_for_search(title)), stored_text_fieldtype))
        # parse URLs for their domains
        doc.add(Field('site', urlparse(url).netloc, site_fieldtype))
        doc.add(Field('url', url, unindexed_stored_fieldtype))
        webpage_writer.addDocument(doc)

    # index images
    image_db = sqlite3.connect('crawled/image_list.sqlite')
    cursor = image_db.cursor()
    table_name = cursor.execute(
        'SELECT name FROM sqlite_master '
        'WHERE type=\'table\' ORDER BY name DESC LIMIT 1'
    ).fetchone()[0]
    for row in cursor.execute('SELECT * FROM ' + table_name):
        url, description, origin = row
        print('Adding ' + description)
        doc = Document()

        doc.add(Field('description',
                      ' '.join(jieba.cut_for_search(description)),
                      stored_text_fieldtype))
        doc.add(Field('origin', origin, unindexed_stored_fieldtype))
        doc.add(Field('url', url, unindexed_stored_fieldtype))
        image_writer.addDocument(doc)

    # commit index
    ticker = Ticker()
    print('commit index', end=' ')
    threading.Thread(target=ticker.run).start()
    webpage_writer.commit()
    webpage_writer.close()
    image_writer.commit()
    image_writer.close()
    ticker.tick = False
    print('done')

    end = datetime.now()
    print(end - start)
