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
      slave_ok = settings.get('read_only') and True or False
      connection = pymongo.Connection(mongo_database['host'], mongo_database['port'], slave_okay=slave_ok, network_timeout=2)
      Proxy._db = connection[mongo_database['db']]

    return getattr(self._db, name)

db = Proxy()