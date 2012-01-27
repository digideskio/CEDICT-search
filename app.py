import re
import simplejson

from flask import Flask
from db import THE_DICTIONARY

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
        THE_DICTIONARY.find({'english_full': regex}, {'_id': 0})
        )

    return simplejson.dumps(results_list, indent=4)

@app.route('/')
def index():
    print 'hello world'

if __name__ == '__main__':
    app.run()
