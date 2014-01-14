# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/AlexanderPease/git/usv/website/usv')
import settings

from lib import jobsdb

''' Requires a country argument to run '''
country = sys.argv[1]
jobsdb.update_country(country) 

