import sys
try:
	sys.path.insert(0, '/Users/nick/dev/theconversation')
except:
	pass

from lib import userdb

users = userdb.get_all()

for user in users:
	user['email_address'] = ""
	user['disqus'] = {}
	user['access_token'] = {}
	userdb.save_user(user)
	print "saved user %s" % user['user']['username']