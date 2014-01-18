from bson.son import SON
from mongo import db
from datetime import datetime, timedelta

def get_user_tags(screen_name):
  tags = db.post.aggregate([
    {'$unwind':'$tags'},
    {'$match': {'user.screen_name':screen_name}},
    {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}
  ])
  return tags

def get_all_tags(sort=None):
  if not sort or sort == "count":
    sort = SON([("count", -1), ("_id", -1)])
  if sort == "alpha":
    sort = SON([("_id", 1)])
  
  tags = db.post.aggregate([
    {'$unwind':'$tags'},
    {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
    {"$sort": sort}
  ])
  return tags

def get_hot_tags():
  today = datetime.today()
  two_weeks_ago = today + timedelta(days=-14)
  tags = db.post.aggregate([
    {'$unwind':'$tags'},
    {'$match': {'date_created':{'$gte':two_weeks_ago}}},
    {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])},
    {"$limit": 40}
  ])
  return tags

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
