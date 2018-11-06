import flask
import jieba
import lucene

from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, TermQuery
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search.highlight import (
    SimpleHTMLFormatter, Highlighter, QueryScorer, TokenSources)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
app = flask.Flask(__name__)


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


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/search')
def search():
    user_query = flask.request.args['q']
    lucene.getVMEnv().attachCurrentThread()
    directory = SimpleFSDirectory(File('index/webpages/').toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()

    # In later version of Lucene, BooleanQuery becomes immutable and can
    # only be constructed by BooleanQuery.Builder
    query_builder = BooleanQuery.Builder()
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
    final_query = query_builder.build()
    score_docs = searcher.search(final_query, 10).scoreDocs
    results = []
    for score_doc in score_docs:
        doc = searcher.doc(score_doc.doc)
        with open('crawled/text/' + doc.get('filename')) as f:
            text = ' '.join(jieba.cut_for_search(f.read()))

        html_formatter = SimpleHTMLFormatter('<em>', '</em>')
        highlighter = Highlighter(html_formatter, QueryScorer(final_query))
        index_reader = searcher.getIndexReader()
        token_stream = TokenSources.getTokenStream(
            'content', index_reader.getTermVectors(score_doc.doc),
            text, analyzer,
            highlighter.getMaxDocCharsToAnalyze() - 1
        )
        frag = highlighter.getBestFragment(token_stream, text)
        results.append((doc.get('title'), flask.Markup(frag)))
    return flask.render_template('search.html', results=results)


@app.route('/image')
def image_search():
    user_query = flask.request.args['q']
    lucene.getVMEnv().attachCurrentThread()
    directory = SimpleFSDirectory(File('index/images/').toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()

    query = QueryParser('description', analyzer).parse(
        ' '.join(jieba.cut(user_query)))
    top_docs = searcher.search(query, 10).scoreDocs

    results = []
    for score_doc in top_docs:
        doc = searcher.doc(score_doc.doc)
        results.append((doc.get('url'), doc.get('description'), doc.get('origin')))
    return str(results)
