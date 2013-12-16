from mongo import db

# For update_twitter
import tweepy
import settings

"""
{
  'user': { 'id_str':'', 'auth_type': '', 'username': '', 'fullname': '', 'screen_name': '', 'profile_image_url_https': '', 'profile_image_url': '', 'is_blacklisted': False }
  'access_token': { 'secret': '', 'user_id': '', 'screen_name': '', 'key': '' },
  'email_address': '',
  'role': '',
  'tags':[]
}

"""

''' Returns all users '''
def get_all():
  return db.user_info.find()

def get_user_by_id_str(id_str):
  return db.user_info.find_one({'user.id_str': id_str})

def get_user_by_screen_name(screen_name):
  return db.user_info.find_one({'user.screen_name': screen_name})

def get_user_by_email(email_address):
  return db.user_info.find_one({'email_address':email_address})

def create_new_user(user, access_token):
  return db.user_info.update({'user.id_str': user['id_str']}, {'user':user, 'access_token':access_token, 'email_address':'', 'role':''}, upsert=True)

def save_user(user):
  return db.user_info.update({'user.id_str': user['user']['id_str']}, user)

def get_user_count():
  return db.user_info.count()

def add_tags_to_user(screen_name, tags=[]):
  return db.user_info.update({'user.screen_name':screen_name}, {'$addToSet':{'tags':{'$each':tags}}})

''' Update all account info from twitter, i.e. profile pic '''
def update_twitter_all():
  consumer_key = settings.get('twitter_consumer_key')
  consumer_secret = settings.get('twitter_consumer_secret')
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  api = tweepy.API(auth) 

  for user in get_all():
    id_str = user['user']['id_str']
    twitter_user = api.get_user(id=id_str)
    if id_str != twitter_user.id_str:
      raise Exception

    user_data = {
      'auth_type': 'twitter',
      'id_str': twitter_user.id_str,
      'username': twitter_user.screen_name,
      'fullname': twitter_user.name,
      'screen_name': twitter_user.screen_name,
      'profile_image_url': twitter_user.profile_image_url,
      'profile_image_url_https': twitter_user.profile_image_url_https,
    }

    updated_user = {'access_token': user['access_token'], 'user': user_data}
    save_user(updated_user)
    print "Updated user @%s" % user['user']['username']

