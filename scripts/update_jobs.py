# Run by Heroku scheduler every night
from lib import jobsdb

jobsdb.update_all() 