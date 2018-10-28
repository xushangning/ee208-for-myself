import jieba
import lucene
from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, TermQuery
from org.apache.lucene.store import SimpleFSDirectory


def parse_query(query):
    """
    Parse queries in the form "<term>* (<field>:<term>)*" to a dict
    :param query: str. Terms whose field is not specified will be gathered in
    the "default" field
    :return: dict
    """
    allowed_fields = {'title', 'content', 'site'}
    query_dict = {}
    for i in query.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            # Currently, if there are multiple occurrences of the same field,
            # only the last term will be added to the query.
            if opt in allowed_fields and len(value):
                query_dict[opt] = value
        else:
            # gather terms without fields under the "default" key
            query_dict['default'] = query_dict.get('default', '') + ' ' + i
    return query_dict


if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()

    # gathering all field names together for output formatting later
    field_names = ('url', 'title', 'site', 'filename')
    while True:
        print()
        print("Hit enter with no input to quit.")
        command = input("Query:")
        if command == '':
            break

        print('\nSearching for:', command)
        # In later version of Lucene, BooleanQuery becomes immutable and can
        # only be constructed by BooleanQuery.Builder
        query_builder = BooleanQuery.Builder()
        query_dict = parse_query(command)
        if query_dict.get('default') is not None:
            terms = ' '.join(jieba.cut(query_dict['default']))
            # search over "content" and "title' fields
            query = QueryParser('content', analyzer).parse(terms)
            query_builder.add(query, BooleanClause.Occur.SHOULD)
            query = QueryParser('title', analyzer).parse(terms)
            query_builder.add(query, BooleanClause.Occur.SHOULD)
        if query_dict.get('site') is not None:
            # use TermQuery because we expect an exact match
            query_builder.add(TermQuery(Term('site', query_dict['site'])),
                              BooleanClause.Occur.MUST)
        # build a BooleanQuery object and pass it to searcher
        # retrieve the top 20 hits
        scoreDocs = searcher.search(query_builder.build(), 20).scoreDocs

        print(len(scoreDocs), 'total matching documents.')
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            for n in field_names:
                # get the value stored in the field
                print(n + ':', doc.get(n))
            print('score:', scoreDoc.score, end='\n\n')
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
