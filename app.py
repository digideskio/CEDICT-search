import re
import simplejson

from flask import Flask
from db import THE_DICTIONARY

MAX_RESULTS = 200

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
        return result[search_field].index(words[0])

    def get_portion(result):
        'a good result has some definition where the query is a large % of the total definition'
        if search_field == 'english_full':
            candidates = [s.lower() for s in result['english_list']]
        else:
            candidates = [result[search_field]]

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

    regex_str = query.replace(' ', '.*')
    regex = re.compile(regex_str, re.UNICODE | re.IGNORECASE)

    results_list = list(
        THE_DICTIONARY.find({'english_full': regex}, {'_id': 0}).limit(MAX_RESULTS)
        )

    search_field = 'english_full'
    search_field_display = 'English'

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
