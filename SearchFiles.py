import jieba
import lucene
from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause
from org.apache.lucene.store import SimpleFSDirectory

if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()

    field_names = ('url', 'title', 'site', 'filename')
    while True:
        print()
        print("Hit enter with no input to quit.")
        command = input("Query:")
        if command == '':
            break

        print('\nSearching for:', command)
        query_builder = BooleanQuery.Builder()
        command = ' '.join(jieba.cut(command))
        query = QueryParser('content', analyzer).parse(command)
        query_builder.add(query, BooleanClause.Occur.SHOULD)
        query = QueryParser('title', analyzer).parse(command)
        query_builder.add(query, BooleanClause.Occur.SHOULD)
        scoreDocs = searcher.search(query_builder.build(), 20).scoreDocs

        print(len(scoreDocs), 'total matching documents.')
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            for n in field_names:
                print(n + ':', doc.get(n))
            print('score:', scoreDoc.score, end='\n\n')
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
