try:
	import sys
	sys.path.insert(0, '/Users/nick/dev/theconversation')
except:
	print "could not import -- must be running on heroku"

from customerio import CustomerIO
import settings
from lib import userdb

cio = CustomerIO(settings.get('customer_io_site_id'), settings.get('customer_io_api_key'))

users = userdb.get_all()
for user_info in users:
	if user_info and 'user' in user_info.keys() and 'email_address' in user_info.keys() and user_info['email_address'] != "":
		cio.identify(id=user_info['user']['username'], email=user_info['email_address'], name=user_info['user']['fullname'])
		print "added @" + user_info['user']['username']