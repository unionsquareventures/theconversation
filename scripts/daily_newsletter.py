# Run by Heroku Scheduler every 10min
from datetime import datetime, timedelta
try:
	import sys
	sys.path.insert(0, '/Users/nick/dev/conversation')
except:
	print "could not import -- must be running on heroku"

from lib import postsdb, emailsdb


# 1) get 5 slugs
posts = postsdb.get_hot_posts_by_day(datetime.today())
slugs = []
for i, post in enumerate(posts):
	if i < 5:
		slugs.append(post['slug'])

# 2) construct email
email = emailsdb.construct_daily_email(slugs)

# 3) send it
result = emailsdb.send_daily_email(email)