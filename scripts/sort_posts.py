# Run by Heroku Scheduler every 5min
from lib import postsdb

postsdb.sort_posts()

