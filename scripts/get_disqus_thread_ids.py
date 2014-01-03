# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/nick/dev/conversation')
import settings
import requests

from lib import postsdb
from lib import disqus
from lib import userdb

#
# for a single user, get disqus thread IDs for their posts
#

threads = disqus.subscribe_to_all_your_threads('aweissman')