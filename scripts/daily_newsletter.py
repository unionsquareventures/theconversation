<<<<<<< HEAD
=======
# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
import settings
import requests
import logging
from datetime import datetime

from lib import postsdb, emailsdb
import csv

# 1) get 5 slugs
posts = postsdb.get_hot_posts_by_day(datetime.today())
slugs = []
for i, post in enumerate(posts):
	if i < 5:
		slugs.append(post['slug'])

# 2) construct email
#request1 = emailsdb.construct_daily_email(slugs)

# Setup list for the day
#if request1['message'] == "success":
#	request2 = emailsdb.setup_email_list()

# Add list to email
#if request2['message'] == "success":
request3 = emailsdb.add_list_to_email()

# 3) send it
if request3['message'] == "success":
	print "READY!"
#result = emailsdb.send_daily_email(email)
>>>>>>> 3393380... hopefully functioning daily email scripts
