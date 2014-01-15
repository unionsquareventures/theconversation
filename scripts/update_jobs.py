# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/AlexanderPease/git/usv/website/usv')
import settings

from lib import jobsdb

INDEED_COUNTRIES = ['US',
					'GB', # Great Britain
					'CA',
					'DE',
					'IL', # Israel
					'FR',
					'NL', # Netherlands
					'SE', # Sweden
					'IE', # Ireland
					'JP'] # Japan

''' Requires a country argument to run. Must be uppercase '''
country = sys.argv[1]
jobsdb.update_country(country) 

