import logging
import pymongo
import settings


class Proxy(object):
  _db = None
  def __getattr__(self, name):
    if Proxy._db == None:
      # lazily connect to the db so we pickup the right environment settings
      mongo_database = settings.get('mongo_database')
      logging.info("connecting to mongo at %s:%d/%s" % (mongo_database['host'], mongo_database['port'], mongo_database['db']))
      connection = pymongo.MongoClient(mongo_database['host'], mongo_database['port'], connectTimeoutMS=5000, max_pool_size=200)
      Proxy._db = connection[mongo_database['db']]

    return getattr(self._db, name)

db = Proxy()