import logging
import pymongo

class Proxy(object):
    _db = None
    def __getattr__(self, name):
        if Proxy._db == None:
            # lazily connect to the db so we pickup the right environment settings
            logging.info("connecting to mongo at %s:%d/%s" % ('localhost', 27017, 'usv'))
            connection = pymongo.MongoClient('localhost', 27017, connectTimeoutMS=5000, max_pool_size=200)
            Proxy._db = connection['usv']

        return getattr(self._db, name)

db = Proxy()
