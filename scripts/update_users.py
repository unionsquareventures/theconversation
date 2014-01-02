# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
import settings

from lib import userdb

userdb.update_twitter_profile_images() 
