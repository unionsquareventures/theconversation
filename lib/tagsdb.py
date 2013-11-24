from bson.son import SON
from mongo import db

def get_user_tags(screen_name):
  tags = db.post.aggregate([
    {'$unwind':'$tags'},
    {'$match': {'user.screen_name':screen_name}},
    {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}
  ])
  return tags

def save_tag(tag):
  return db.tag.update({'name':tag}, {'name':tag}, upsert=True)
