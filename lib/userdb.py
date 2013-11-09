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
  return {}

def save_user(user, access_token):
  return