# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/nick/dev/conversation')
import settings

from lib import postsdb
from lib import disqus
from mongo import db

#users = db.user_info.find({"lastname" : {"$exists" : true, "$ne" : ""}})
threads = disqus.get_all_threads()

for thread in threads['response']:
	print(thread)
	#for key in thread['response'].keys():
	#	logging.info(key + ": " + thread[key])