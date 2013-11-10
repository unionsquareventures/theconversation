import pymongo
import re
import settings
import time

from datetime import datetime
from math import log
from mongo import db
from slugify import slugify

"""
'indexes': ['-date_deleted', 'deleted', '-date_featured', 'votes', 'date_created', 'featured', 'voted_users', 'user.id_str', 'slug', 'slugs', 'url', 'tags', 'normalized_url'],

{
  'date_created':new Date(),
  'title': '',
  'slugs': [],
  'slug': '',
  'user': { 'id_str':'', 'auth_type': '', 'username': '', 'fullname': '', 'screen_name': '', 'profile_image_url_https': '', 'profile_image_url': '', 'is_blacklisted': False },
  'tags': [],
  'votes': 0,
  'voted_users': [{ 'id_str':'', 'auth_type': '', 'username': '', 'fullname': '', 'screen_name': '', 'profile_image_url_https': '', 'profile_image_url': '', 'is_blacklisted': False }],
  'deleted': False,
  'date_deleted': new Date(),
  'featured': False
  'date_featured': new Date(),
  'url': '',
  'normalized_url': '',
  'hackpad_url': '',
  'has_hackpad': False,
  'body_raw': '',
  'body_html': '',
  'body_truncated': '',
  'body_text': '',
  'disqus_shortname': 'usvbeta2',
  'muted': False,
  'comment_count': 0,
  'disqus_thread_id_str': '',
  'sort_score': 0.0,
  'downvotes': 0,
}
"""

def get_latest_staff_posts_by_tag(tag, limit=10):
  staff = settings.get('staff')
  return list(db.post.find({'user.username': {'$in': staff}, 'tags':tag}, sort=[('date_featured', pymongo.DESCENDING)]).limit(limit))

def get_posts_by_query(query, per_page=10, page=1):
  query_regex = re.compile('%s[\s$]' % query, re.I)
  return list(db.post.find({'$or':[{'title':query_regex}, {'body_raw':query_regex}]}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_post_count_by_query(query):
  query_regex = re.compile('%s[\s$]' % query, re.I)
  return len(list(db.post.find({'$or':[{'title':query_regex}, {'body_raw':query_regex}]})))

def get_posts_by_tag(tag, per_page=10, page=1):
  return list(db.post.find({'tags':tag}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_post_count_by_tag(tag):
  return len(list(db.post.find({'tags':tag})))

def get_featured_posts(limit):
  return list(db.post.find({'featured':True}, sort=[('date_featured', pymongo.DESCENDING)]).limit(limit))

def get_new_posts(per_page=50, page=1):
  return list(db.post.find({}, sort=[('_id', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_hot_posts():
  # hot posts are calculated out of the last 'hot_post_set_count' posts
  hot_post_set_count = settings.get('hot_post_set_count')
  posts = list(db.post.find({}, sort=[('_id', pymongo.DESCENDING)]).limit(hot_post_set_count))
  # now calculate a rank for each post in this set
  for post in posts:
    adjusted_votes = log(max(abs(post['votes']), 1), 10)
    sign = 1
    age_factor = 45000.0 # ~12.5 hour increments
    timestamp = time.mktime(post['date_created'].timetuple())
    post['score'] = adjusted_votes + round(sign * timestamp / age_factor)

  # finally sort the posts by the newly added 'score' field
  try:
    posts = sorted(posts, key=lambda k: k['score'])
    posts.reverse()
  except:
    posts = posts

  return posts

def get_sad_posts(per_page=50, page=1):
  return list(db.post.find({'date_created':{'$gt': datetime.strptime("10/12/13", "%m/%d/%y")}, 'votes':0, 'comment_count':0, 'deleted': False, 'featured': False}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_posts_by_normalized_url(normalized_url, limit):
  return list(db.post.find({'normalized_url':normalized_url, 'deleted':False}, sort=[('_id', pymongo.DESCENDING)]).limit(limit))

def get_post_by_slug(slug):
  return db.post.find_one({'slug':slug})

def insert_post(post):
  slug = slugify(post['title'])
  slug_count = len(list(db.post.find({'slug':slug})))
  if slug_count > 0:
    slug = '%s-%i' % (slug, slug_count)
  post['slug'] = slug
  post['slugs'] = [slug]
  return db.post.update({'url':post['slug'], 'user.screen_name':post['user']['screen_name']}, post, upsert=True)

def save_post(post):
  return db.post.update({'_id':post['_id']}, post)
