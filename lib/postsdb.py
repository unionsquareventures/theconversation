import pymongo
import re
import settings

from datetime import datetime
from mongo import db
from slugify import slugify
import userdb

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
### GET ALL POSTS
###########################
def get_all():
  return db.post.find()

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
  return list(db.post.find({'deleted': { "$ne": True }, 'tags':tag}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_posts_by_screen_name(screen_name, per_page=10, page=1):
  return list(db.post.find({'deleted': { "$ne": True }, 'user.screen_name':screen_name}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_posts_by_screen_name_and_tag(screen_name, tag, per_page=10, page=1):
  return list(db.post.find({'deleted': { "$ne": True }, 'user.screen_name':screen_name, 'tags':tag}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_featured_posts(per_page=10, page=1):
  return list(db.post.find({'deleted': { "$ne": True }, 'featured':True}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_new_posts(per_page=50, page=1):
  return list(db.post.find({"deleted": { "$ne": True }}, sort=[('_id', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

def get_hot_posts(per_page=50, page=1):
  posts = list(db.post.find({"votes": { "$gte" : 2 }, "deleted": { "$ne": True }}, sort=[('sort_score', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))
  return posts

def get_sad_posts(per_page=50, page=1):
  return list(db.post.find({'date_created':{'$gt': datetime.strptime("10/12/13", "%m/%d/%y")}, 'votes':1, 'comment_count':0, 'deleted': { "$ne": True } , 'featured': False}, sort=[('date_created', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page))

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
  return list(db.post.find({'deleted': { "$ne": True }, 'user.username': {'$in': staff}, 'tags':tag}, sort=[('date_featured', pymongo.DESCENDING)]).limit(limit))

def get_posts_by_normalized_url(normalized_url, limit):
  return list(db.post.find({'normalized_url':normalized_url, 'deleted': { "$ne": True }}, sort=[('_id', pymongo.DESCENDING)]).limit(limit))

def get_posts_with_min_votes(min_votes):
  return list(db.post.find({'deleted': { "$ne": True }, 'votes':{'$gte':min_votes}}, {'slug':1, 'date_created':1, 'downvotes':1, 'user.username':1, 'comment_count':1, 'votes':1, 'title':1}, sort=[('date_created', pymongo.DESCENDING)]))

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


###########################
### SORT ALL POSTS
### RUN BY HEROKU SCHEDULER EVERY 5 MIN
### VIA SCRIPTS/SORT_POSTS.PY
###########################
def sort_posts():
  # set our config values up
  #staff_bonus = int(self.get_argument('staff_bonus', -3))
  staff_bonus = -3
  #time_penalty_multiplier = float(self.get_argument('time_penalty_multiplier', 2.0))
  time_penalty_multiplier = 2.0
  #grace_period = float(self.get_argument('grace_period', 6.0))
  grace_period = 6.0
  #comments_multiplier = float(self.get_argument('comments_multiplier', 3.0))
  comments_multiplier = 3.0
  #votes_multiplier = float(self.get_argument('votes_multiplier', 1.0))
  votes_multiplier = 1.0
  #min_votes = float(self.get_argument('min_votes', 2))
  min_votes = 2

  # get all the posts that have at least the 'min vote threshold'
  posts = get_posts_with_min_votes(min_votes)

  data = []
  for post in posts:
    # determine how many hours have elapsed since this post was created
    tdelta = datetime.now() - post['date_created']
    hours_elapsed = tdelta.seconds/3600 + tdelta.days*24

    # determine the penalty for time decay
    time_penalty = 0
    if hours_elapsed > grace_period:
      time_penalty = hours_elapsed - grace_period
    if hours_elapsed > 12:
      time_penalty = time_penalty * 1.5
    if hours_elapsed > 18:
      time_penalty = time_penalty * 2

    # get our base score from downvotes
    #base_score = post['downvotes'] * -1
    base_score = 0

    # determine if we should assign a staff bonus or not
    if post['user']['username'] in settings.get('staff'):
      staff_bonus = staff_bonus
    else:
      staff_bonus = 0

    # determine how to weight votes
    votes_base_score = 0
    if post['votes'] == 1 and post['comment_count'] > 2:
      votes_base_score = -2
    if post['votes'] > 8 and post['comment_count'] == 0:
      votes_base_score = -2

    scores = {}
    # now actually calculate the score
    total_score = base_score
    
    scores['votes'] = (votes_base_score + post['votes'] * votes_multiplier)
    total_score += scores['votes']
    
    scores['comments'] = (post['comment_count'] * comments_multiplier)
    total_score += scores['comments']
    
    scores['time'] = (time_penalty * time_penalty_multiplier * -1)
    total_score += scores['time']
    
    total_score += staff_bonus
    post['scores'] = scores

    # and save the new score
    update_post_score(post['slug'], total_score)

    data.append({
      'username': post['user']['username'],
      'title': post['title'],
      'slug': post['slug'],
      'date_created': post['date_created'],
      'hours_elapsed': hours_elapsed,
      'votes': post['votes'],
      'comment_count': post['comment_count'],
      'staff_bonus': staff_bonus,
      'time_penalty': time_penalty,
      'total_score': total_score,
      'scores': scores
    })

  data = sorted(data, key=lambda k: k['total_score'], reverse=True)
  print "All posts sorted!"

###########################
### UPDATES USER DATA FOR ALL POSTS
### RUN VIA SCRIPTS/UPDATE_POSTS_USER_DATA.PY
###########################
def update_posts_user_data():
  print "Updating user data for all posts..."
  for post in get_all():
    # user
    try: 
      user = post['user']
      if user:
          new_user = userdb.get_user_by_id_str(user['id_str'])
          post['user'] = new_user['user']
    except: 
      print "Failed to update user for post of slug %s" % post['slug']

    # voted_users
    try: 
      voted_users = post['voted_users']
      new_voted_users = []
      for voted_user in voted_users:
        new_voted_user = userdb.get_user_by_id_str(voted_user['id_str'])
        if new_voted_user:
          new_voted_users.append(new_voted_user['user'])
      post['voted_users'] = new_voted_users
    except:
      print "Failed to update voted_users for post of slug %s" % post['slug']

    # Save post
    save_post(post)
 
  print "Finished updating user data for all posts"









