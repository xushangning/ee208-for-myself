import jieba
import lucene
from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, TermQuery
from org.apache.lucene.store import SimpleFSDirectory


if __name__ == '__main__':
    STORE_DIR = 'index/images/'
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()

    field_names = ('url', 'description', 'origin')
    while True:
        print()
        print("Hit enter with no input to quit.")
        command = input("Query:")
        if command == '':
            break

        print('\nSearching for:', command)
        query = QueryParser('description', analyzer).parse(' '.join(jieba.cut(command)))
        scoreDocs = searcher.search(query, 20).scoreDocs

        print(len(scoreDocs), 'total matching documents.')
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            for n in field_names:
                print(n + ':', doc.get(n))
            print('score:', scoreDoc.score, end='\n\n')
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
