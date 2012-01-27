import pymongo

INDEX_DIR = 'the_index'

MONGO_CONNECTION = pymongo.Connection()
DB = MONGO_CONNECTION.test
THE_DICTIONARY = DB.cedict
