import lucene
import os
import sys
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


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir).toPath())
        analyzer = WhitespaceAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(writer)
        ticker = Ticker()
        print('commit index', end=' ')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    def indexDocs(self, writer):

        filename_fieldtype = FieldType()
        filename_fieldtype.setStored(True)
        filename_fieldtype.setTokenized(False)
        
        content_fieldtype = FieldType()
        content_fieldtype.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        title_fieldtype = FieldType(content_fieldtype)
        title_fieldtype.setStored(True)

        site_fieldtype = FieldType()
        site_fieldtype.setStored(True)
        site_fieldtype.setTokenized(False)
        site_fieldtype.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        index_file = open('crawled/index.txt')
        for line in index_file:
            try:
                url, filename, title = line.rstrip('\n').split('\t')
            # Unpacking errors come from spaces in URLs.
            except ValueError:          # skip unpacking error
                continue
            print('Adding ' + filename)
            doc = Document()

            with open('crawled/text/' + filename, 'r') as f:
                try:
                    content = ' '.join(jieba.cut_for_search(f.read()))
                except UnicodeDecodeError:
                    continue            # skip decoding errors
                doc.add(Field('content', content, content_fieldtype))
            doc.add(Field('filename', filename, filename_fieldtype))
            doc.add(Field('title', ' '.join(jieba.cut_for_search(title)), title_fieldtype))
            doc.add(Field('site', urlparse(url).netloc, site_fieldtype))
            doc.add(Field('url', url, filename_fieldtype))
            writer.addDocument(doc)


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        IndexFiles('index')
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
