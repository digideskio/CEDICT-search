import re
import simplejson
import jianfan

from flask import Flask
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from db import THE_DICTIONARY, INDEX_DIR

from query_detection import is_cjk, is_pinyin

MAX_RESULTS = 200

# whoosh is really only helpful for english here (and maybe pinyin.) two reasons:
# 1. our source is a chinese -> english dictionary. with text indexing on english we can make it go both ways.
# 2. chinese characters don't have spaces, so without segmentation our indexer wouldn't know how to break them into words to begin with.
whoosh_idx = open_dir(INDEX_DIR)
searcher = whoosh_idx.searcher()
query_parser = QueryParser('english_full', whoosh_idx.schema)

app = Flask(__name__)
app.debug = True ## DON'T LAUNCH THIS TO THE PUBLIC

def make_cmp(query, search_field):
    '''
    returns a function cmp(r1, r2), that returns a negative int if r1 should be sorted before r2,
    0 if they're the same relevance, and positive if r1 > r2.
    '''
    words = query.split()

    def get_position(result):
        'a good result has the query occuring early'
        return normalize(result[search_field]).index(words[0])

    def get_portion(result):
        'a good result has some definition where the query is a large % of the total definition'
        if search_field == 'english_full':
            candidates = [normalize(s) for s in result['english_list']]
        else:
            candidates = [normalize(result[search_field])]
        # comparators need to return integers, so, scale up the ratios to avoid rounding error.
        # whether this is 100 or 100000 doesn't matter. (it's effectively the # of significant figures.)
        scale = 100
        max_portion = 0
        for candidate in candidates:
            if all(word in candidate for word in words):
                portion = scale * sum(len(word) for word in words) / len(candidate)
                max_portion = max(portion, max_portion)
        return max_portion

    def _cmp(r1, r2): # note: cmp is a predefined python function, so use _cmp
        portion1, portion2 = (get_portion(r) for r in (r1, r2))
        position1, position2 = (get_position(r) for r in (r1, r2))
        if portion1 != portion2:
            return portion2 - portion1
        else:
            return position1 - position2

    return _cmp

def normalize(query):
    return ' '.join(query.lower().strip().split())

@app.route('/search/<query>')
def search(query):
    query = normalize(query)

    if is_cjk(query):
        search_field = 'simplified'
        search_field_display = 'Hanzi'

        # we can support both traditional and simplified queries, by converting traditional to simplified.
        # (traditional->simplified is many to one, which means it's much harder to go the other way.)
        # luckily someone make a pip-installable library jianfan!
        query = jianfan.ftoj(query)
    elif is_pinyin(query):
        search_field = 'pinyin'
        search_field_display = 'Pinyin'
    else:
        search_field = 'english_full'
        search_field_display = 'English'

    results_list = []
    if search_field == 'english_full':
        whoosh_q = query_parser.parse(query)
        whoosh_results_list = searcher.search(whoosh_q)
        # whoosh returns dictionary-like Hit objects. convert to explicit dictionaries.
        whoosh_results_list = [dict(result) for result in whoosh_results_list]
        results_list.extend(whoosh_results_list)

    if not results_list: # only resort to mongo scanning if no results found yet.
        regex_str = query.replace(' ', '.*')
        # note: typically you want to escape user-generated strings before turning them into regexes.
        # in this case, i don't care.
        regex = re.compile(regex_str, re.UNICODE | re.IGNORECASE)

        results_list.extend(list(
            THE_DICTIONARY.find({search_field: regex}, {'_id': 0}).limit(MAX_RESULTS)
            ))

    # comment out this line to see the effect of search result ranking.
    results_list.sort(cmp=make_cmp(query, search_field))

    results = dict(
        results = results_list,
        count = len(results_list),
        search_type = search_field_display,
        )

    return simplejson.dumps(results, indent=4)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
