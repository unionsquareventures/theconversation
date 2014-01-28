# Run by Heroku Scheduler every 10min
from datetime import datetime, timedelta
try:
	import sys
	sys.path.insert(0, '/Users/nick/dev/conversation')
except:
	print "could not import -- must be running on heroku"

from lib import postsdb

postsdb.sort_posts(datetime.today())