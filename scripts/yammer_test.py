# Run by Heroku Scheduler every 10min
import sys
sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
from lib import yammer

yammer.get_networks('nickgrossman')

