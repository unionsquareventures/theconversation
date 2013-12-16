# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/AlexanderPease/git/usv/website/usv')
import settings

from lib import userdb

userdb.update_twitter_all() 