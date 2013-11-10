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
  'hot_post_set_count': 200,
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
  ],
  # define the various roles and what capabilities they support
  'staff_capabilities': [
    'see_admin_link',
    'delete_users',
    'delete_posts',
    'post_rich_media',
    'feature_posts',
    'edit_posts',
    'upvote_multiple_times',
    'super_upvote_posts',
    'downvote_posts'
  ],
  'user_capabilities': []
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

