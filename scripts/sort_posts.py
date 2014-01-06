# Run by Heroku Scheduler every 10min
from lib import postsdb

postsdb.sort_posts()