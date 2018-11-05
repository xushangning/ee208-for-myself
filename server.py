import web
import jieba
import lucene

from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, TermQuery
from org.apache.lucene.store import SimpleFSDirectory

urls = (
    '/', 'Index',
    '/search', 'Search'
)
render = web.template.render('templates/', base='base')

search_box = web.form.Form(web.form.Textbox('q', web.form.notnull))


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


class Index:
    def GET(self):
        return render.index()


class Search:
    def GET(self):
        search_box_copy = search_box()
        if search_box_copy.validates():
            lucene.getVMEnv().attachCurrentThread()
            directory = SimpleFSDirectory(File('index/webpages/').toPath())
            searcher = IndexSearcher(DirectoryReader.open(directory))
            analyzer = WhitespaceAnalyzer()

            # In later version of Lucene, BooleanQuery becomes immutable and can
            # only be constructed by BooleanQuery.Builder
            query_builder = BooleanQuery.Builder()
            user_query = search_box_copy['q'].value
            query_dict = parse_query(user_query)
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
            # retrieve the top 10 hits
            score_docs = searcher.search(query_builder.build(), 10).scoreDocs
            results = []
            for score_doc in score_docs:
                doc = searcher.doc(score_doc.doc)
                results.append((doc.get('title'),))
            return render.search(results)
        else:
            raise web.notfound()


if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    app = web.application(urls, globals())
    app.run()
