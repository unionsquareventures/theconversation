from mongo import db

"""
{
  'user': { 'id_str':'', 'auth_type': '', 'username': '', 'fullname': '', 'screen_name': '', 'profile_image_url_https': '', 'profile_image_url': '', 'is_blacklisted': False }
  'access_token': { 'secret': '', 'user_id': '', 'screen_name': '', 'key': '' },
  'email_address': '',
  'role': ''
}

"""

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