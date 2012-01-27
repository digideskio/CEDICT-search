import re
import simplejson

from flask import Flask
from db import THE_DICTIONARY

MAX_RESULTS = 200

app = Flask(__name__)
app.debug = True ## DON'T LAUNCH THIS TO THE PUBLIC

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

    results = dict(
        results = results_list,
        count = len(results_list),
        search_type = 'English',
        )

    return simplejson.dumps(results, indent=4)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
