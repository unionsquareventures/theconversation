import sys
sys.path.insert(0, '/Users/nick/dev/conversation')
import settings
from lib import postsdb
from lib import userdb
from mongo import db
import logging

#
# MIGRATES from the old voted users format
# to the new one.
# meant to be run by hand from the command line, e.g. python voted_users.py
# Update the path above to whatever path is right on your machine (root of this app)
#


posts = postsdb.get_posts_by_query("", 3000)

for post in posts:
    voted_users = []
    for v in post['voted_users']:
        # OLD FORMAT
        if '_id' in v:
            user_info = userdb.get_user_by_id_str(v['_id'])
            if user_info:
                voted_users.append(user_info['user'])
        # NEW FORMAT
        if 'id_str' in v:
            user_info = userdb.get_user_by_id_str(v['id_str'])
            if user_info:
                voted_users.append(user_info['user'])

    if db.post.update({'_id':post['_id']}, {'$set': {'voted_users': voted_users, 'votes': len(voted_users)}}):
        print('saved post: [%s votes] %s' % (str(len(voted_users)), post['title']))
