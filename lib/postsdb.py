import pymongo
import re
import settings

from datetime import datetime
from mongo import db
from slugify import slugify

"""
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
  'subscribed':[]
}
"""

###########################
### GET A SPECIFIC POST
###########################
def get_post_by_slug(slug):
  return db.post.find_one({'slug':slug})

###########################
### GET PAGED LISTING OF POSTS
###########################
def get_posts_by_bumps(screen_name, per_page, page):
  return list(db.post.find({'voted_users.screen_name':screen_name, 'user.screen_name':{'$ne':screen_name}}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_posts_by_query(query, per_page=10, page=1):
  query_regex = re.compile('%s[\s$]' % query, re.I)
  return list(db.post.find({'$or':[{'title':query_regex}, {'body_raw':query_regex}]}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_posts_by_tag(tag, per_page=10, page=1):
  return list(db.post.find({'tags':tag}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_posts_by_screen_name(screen_name, per_page=10, page=1):
  return list(db.post.find({'user.screen_name':screen_name}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_posts_by_screen_name_and_tag(screen_name, tag, per_page=10, page=1):
  return list(db.post.find({'user.screen_name':screen_name, 'tags':tag}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_featured_posts(per_page=10, page=1):
  return list(db.post.find({'featured':True}, sort=[('date_featured', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_new_posts(per_page=50, page=1):
  return list(db.post.find({}, sort=[('_id', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_hot_posts(per_page=50, page=1):
  posts = list(db.post.find({"votes": { "$gte" : 2 }}, sort=[('sort_score', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))
  return posts

def get_sad_posts(per_page=50, page=1):
  return list(db.post.find({'date_created':{'$gt': datetime.strptime("10/12/13", "%m/%d/%y")}, 'votes':1, 'comment_count':0, 'deleted': False, 'featured': False}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_deleted_posts(per_page=50, page=1):
  return list(db.post.find({'deleted':True}, sort=[('date_deleted', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

###########################
### AGGREGATE QUERIES
###########################
def get_unique_posters(start_date, end_date):
  return db.post.group(["user.screen_name"], {'date_created':{'$gte': start_date, '$lte': end_date}}, {"count":0}, "function(o, p){p.count++}" )

###########################
### GET POST COUNTS
###########################
def get_featured_posts_count():
  return len(list(db.post.find({'featured':True})))

def get_post_count_by_query(query):
  query_regex = re.compile('%s[\s$]' % query, re.I)
  return len(list(db.post.find({'$or':[{'title':query_regex}, {'body_raw':query_regex}]})))

def get_post_count():
  return len(list(db.post.find({'date_created':{'$gt': datetime.strptime("10/12/13", "%m/%d/%y")}})))

def get_post_count_for_range(start_date, end_date):
  return len(list(db.post.find({'date_created':{'$gte': start_date, '$lte': end_date}})))

def get_delete_posts_count():
  return len(list(db.post.find({'deleted':True})))

def get_post_count_by_tag(tag):
  return len(list(db.post.find({'tags':tag})))

###########################
### GET LIST OF POSTS BY CRITERIA
###########################
def get_latest_staff_posts_by_tag(tag, limit=10):
  staff = settings.get('staff')
  return list(db.post.find({'user.username': {'$in': staff}, 'tags':tag}, sort=[('date_featured', pymongo.DESCENDING)]).limit(limit))

def get_posts_by_normalized_url(normalized_url, limit):
  return list(db.post.find({'normalized_url':normalized_url, 'deleted':False}, sort=[('_id', pymongo.DESCENDING)]).limit(limit))

def get_posts_with_min_votes(min_votes):
  return list(db.post.find({'deleted':False, 'votes':{'$gt':min_votes}}, {'slug':1, 'date_created':1, 'downvotes':1, 'user.username':1, 'comment_count':1, 'votes':1, 'title':1}, sort=[('date_created', pymongo.DESCENDING)]))

###########################
### UPDATE POST DETAIL
###########################
def add_subscriber_to_post(slug, email):
  return db.post.update({'slug':slug}, {'$addToSet': {'subscribed': email}})

def remove_subscriber_from_post(slug, email):
  return db.post.update({'slug':slug}, {'$pull': {'subscribed': email}})

def save_post(post):
  return db.post.update({'_id':post['_id']}, post)

def update_post_score(slug, score):
  return db.post.update({'slug':slug}, {'$set':{'sort_score': score}})

def delete_all_posts_by_user(screen_name):
  db.post.update({'user.screen_name':screen_name}, {'$set':{'deleted':True, 'date_delated': datetime.utcnow()}}, multi=True)

###########################
### ADD A NEW POST
###########################
def insert_post(post):
  slug = slugify(post['title'])
  slug_count = len(list(db.post.find({'slug':slug})))
  if slug_count > 0:
    slug = '%s-%i' % (slug, slug_count)
  post['slug'] = slug
  post['slugs'] = [slug]
  if 'subscribed' not in post.keys():
    post['subscribed'] = []
  db.post.update({'url':post['slug'], 'user.screen_name':post['user']['screen_name']}, post, upsert=True)
  return post['slug']

