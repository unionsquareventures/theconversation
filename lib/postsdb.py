import settings
import logging
from mongo import db

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
  logging.info(settings.get('staff'))
  return []

def get_posts_by_query(query, per_page=10, page=1):
  return []

def get_post_count_by_query(query):
  return 0

def get_posts_by_tag(tag, per_page=10, page=1):
  return []

def get_post_count_by_tag(tag):
  return 0
