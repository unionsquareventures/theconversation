import tornado.options

tornado.options.define("environment", default="dev", help="environment")

options = {
  'dev' : {
    'mongo_database' : {'host' : 'localhost', 'port' : 27017, 'db' : 'dev'},
  },
  'test' : {
    'mongo_database' : {'host' : '', 'port' : 27017, 'db' : ''},
  },
  'prod' : {
    'mongo_database' : {'host' : '', 'port' : 27017, 'db' : ''},
  }
}

default_options = {
  'read_only' : False,
  'max_simultaneous_connections' : 10,
  'consumer_key' : 'CmBsLlXpRg7OQY9wlRzfA',
  'consumer_secret' : 'pGFyzrXAnNZqtt2UON2RCfs8BMhHIczqn7wIVP3HpQ',
  'staff':[
    "_zachary",
    "alexandermpease",
    "bwats",
    "aweissman",
    "fredwilson",
    "albertwenger",
    "bradusv",
    "nickgrossman",
    "br_ttany",
    "johnbuttrick",
    "christinacaci",
    "garychou"
  ]
}

def get(key):
  env = tornado.options.options.environment
  if env not in options:
    raise Exception("Invalid Environment (%s)" % tornado.options.options.environment)

  v = options.get(env).get(key) or default_options.get(key)

  if callable(v):
    return v

  if v is not None:
    return v

  return default_options.get(key)

