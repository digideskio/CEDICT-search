import os
import codecs

from whoosh.index import create_in
from whoosh.fields import Schema, STORED, TEXT

from db import THE_DICTIONARY, INDEX_DIR

CEDICT_PATH = 'cedict.txt'

WHOOSH_SCHEMA = Schema(
    traditional  = STORED,
    simplified   = STORED,
    pinyin       = STORED,
    english_full = TEXT(stored=True),
    english_list = STORED,
)

def print_entry(*args):
    print '''
full:    %s
trad:    %s
simp:    %s
pinyin:  %s
english_full: %s
english_list: %s
''' % args

def load_data():

    THE_DICTIONARY.remove() # load from scratch each time

    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    idx = create_in(INDEX_DIR, WHOOSH_SCHEMA)
    whoosh_writer = idx.writer()

    for i, line in enumerate(codecs.open(CEDICT_PATH, 'r', 'utf8')):

        if i % 1000 == 0:
            print '.',

        line = line.strip()
        if line.startswith('#'):
            continue # skip comments

        words = line.split()
        traditional, simplified = words[:2]

        pinyin_start = line.index('[')
        pinyin_end = line.index(']')
        pinyin = line[pinyin_start+1:pinyin_end]

        english = line[pinyin_end+1:].strip(' /')

        english_list = english.split('/')
        english_full = english.lower().replace('/', ' ')

        ## for debugging
        ## print_entry(line, traditional, simplified, pinyin, english_full, english_list)

        THE_DICTIONARY.insert(dict(
                traditional  = traditional,
                simplified   = simplified,
                pinyin       = pinyin,
                english_full = english_full,
                english_list = english_list,
                ))

        whoosh_writer.add_document(
                traditional  = traditional,
                simplified   = simplified,
                pinyin       = pinyin,
                english_full = english_full,
                english_list = english_list,
                )

    whoosh_writer.commit()

if __name__ == '__main__':
    load_data()
