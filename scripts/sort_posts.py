# Run by Heroku Scheduler every 10min
import sys
try:
	sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
except:
	print "could not import -- must be running on heroku"
from lib import postsdb

postsdb.sort_posts()

