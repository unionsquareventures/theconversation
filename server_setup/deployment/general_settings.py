import sys
import os, time
import logging

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

base_url = os.environ.get('BASE_URL')

sendgrid_user = os.environ.get('SENDGRID_USER')
sendgrid_secret = os.environ.get('SENDGRID_SECRET')

redis_url = os.environ.get('REDIS_URL')
mongodb_url = os.environ.get('MONGODB_URL')

disqus_apikey = os.environ.get('DISQUS_SHORTNAME')
disqus_public_key = os.environ.get('DISQUS_PUBLIC_KEY')
disqus_secret_key = os.environ.get('DISQUS_SECRET_KEY')

sentry_dsn = os.environ.get('SENTRY_DSN')

hackpad = {
    'oauth_client_id': os.environ.get('HACKPAD_CLIENT_ID'),
    'oauth_secret': os.environ.get('HACKPAD_OAUTH_SECRET'),
    'domain': os.environ.get('HACKPAD_DOMAIN'),
}

tornado_config = {
    'template_path': os.path.join(PROJECT_ROOT, 'ui/templates'),
    'cookie_secret': os.environ.get('COOKIE_SECRET'),
    'static_path': os.path.join(os.path.dirname(__file__), '../../static'),
    'login_url': '/auth/twitter/',
    'xsrf_cookies': True,
    'twitter_consumer_key': os.environ.get('TWITTER_CONSUMER_KEY'),
    'twitter_consumer_secret': os.environ.get('TWITTER_CONSUMER_SECRET'),
}

post_char_limit = 1000

module_dir = os.path.join(PROJECT_ROOT, 'ui/modules')

test_twitter_username = os.environ.get('TEST_TWITTER_USERNAME')
test_twitter_password = os.environ.get('TEST_TWITTER_PASSWORD')

banned_user_ids = [
]

css_file = "%s/css/style.css" % tornado_config['static_path']
css_modified_time = os.path.getmtime(css_file)

#
# legacy-ish.  This is being used by a few queries for getting posts written by usv staff.
staff_twitter_handles = [
    "_zachary",
    "alexandermpease",
    "bwats",
    "aweissman",
    "fredwilson",
    "albertwenger",
    "bradusv",
    "nickgrossman",
    "br_ttany",
    "johnbuttrick",
    "christinacaci",
    "garychou" 
]

#
# Capabilities -- maps roles to things they can do
# Available capabilities:
#   see_admin_link
#   delete_users
#   delete_posts            
#   post_rich_media   
#   feature_posts
#   edit_posts
#   upvote_multiple_times
#   super_upvote_posts
#   downvote_posts
#   mute_posts
#
capabilities = {
    'staff': [
            'see_admin_link',
            'delete_users',
            'delete_posts',
            'post_rich_media',
            'feature_posts',
            'edit_posts',
            'upvote_multiple_times',
            'super_upvote_posts',
            'downvote_posts'
        ],
    'user': []
}