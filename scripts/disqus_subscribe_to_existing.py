# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/nick/dev/conversation')
import settings
import requests
import logging
from lib import postsdb
from lib import disqus
from lib import userdb

# =================================================================
# This script finds all users that have authenticated with Disqus
# and then sweeps back through their disqus threads
# and make sure they are subscribed to all of them.
# =================================================================

#
# Find all users who have disqus_user_ids
#
disqus_users = userdb.get_disqus_users()

#
# for each user, subscribe them to all of their threads
#
for u in disqus_users:
	print u['user']['username']
	print "-- %s" % u['disqus']['user_id']
	disqus.subscribe_to_all_your_threads(u['user']['username'])