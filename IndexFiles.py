import lucene
import os
import sys
import sqlite3
import threading
import time
from datetime import datetime
import jieba

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

    store_dir = 'index/images/'
    if not os.path.exists(store_dir):
        os.mkdir(store_dir)

    # create an index writer
    store = SimpleFSDirectory(File(store_dir).toPath())
    analyzer = WhitespaceAnalyzer()
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    # add documents to the index
    filename_fieldtype = FieldType()
    filename_fieldtype.setStored(True)
    filename_fieldtype.setTokenized(False)

    title_fieldtype = FieldType()
    title_fieldtype.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    title_fieldtype.setStored(True)

    db = sqlite3.connect('index/images/image_index.sqlite')
    cursor = db.cursor()
    for row in cursor.execute('SELECT * FROM indices'):
        url, description, title = row[:3]
        print('Adding ' + description)
        doc = Document()

        doc.add(Field('description',
                      ' '.join(jieba.cut_for_search(description)),
                      title_fieldtype))
        doc.add(Field('title', ' '.join(jieba.cut_for_search(title)), title_fieldtype))
        doc.add(Field('url', url, filename_fieldtype))
        writer.addDocument(doc)

    # commit index
    ticker = Ticker()
    print('commit index', end=' ')
    threading.Thread(target=ticker.run).start()
    writer.commit()
    writer.close()
    ticker.tick = False
    print('done')

    end = datetime.now()
    print(end - start)
