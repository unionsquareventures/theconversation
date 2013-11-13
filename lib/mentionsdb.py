import pymongo

from datetime import datetime
from mongo import db

"""
{
  'screen_name': '',
  'slug': '',
  'date_created': new Date()
}
"""

def add_mention(screen_name, slug):
  return db.mentions.update({'screen_name': screen_name, 'slug': slug}, {'screen_name': screen_name, 'slug': slug, 'date_created': datetime.utcnow()}, upsert=True)

def get_mentions_by_user(screen_name, per_page, page):
  mentions = list(db.mentions.find({'screen_name': screen_name}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))
  posts = []
  for mention in mentions:
    posts.append(db.post.find_one({'slug':mention['slug']}))
  return posts
