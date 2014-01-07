import urllib2
import urllib
import simplejson as json
import tornado.web
import logging
import settings
import app.basic

from lib import userdb
from lib import postsdb

####################
### AUTH VIA YAMMER
### /auth/yammer
####################
class Auth(app.basic.BaseHandler):
	def get(self):
		req_host = self.request.headers['host']
		yammer_client_id = settings.get('yammer_client_id')
		redirect_url = 'https://www.yammer.com/dialog/oauth?client_id=%s&redirect_uri=http://%s/yammer' % (yammer_client_id, req_host)
		self.redirect(redirect_url)

##############################
### RESPONSE FROM YAMMER AUTH
### /yammer
##############################
class Yammer(app.basic.BaseHandler):
	def get(self):
		logging.info('HERE')
		code = self.get_argument('code','')
		#req_host = self.request.headers['host']

		yammer_client_id = settings.get('yammer_client_id')
		yammer_client_secret = settings.get('yammer_client_secret')

		link = 'https://www.yammer.com/oauth2/access_token.json'
		#https://www.yammer.com/api/v1/oauth/tokens.json -- to get multiple tokens
		data = {
			'client_id':yammer_client_id,
			'client_secret':yammer_client_secret,
			'code' : code
		}
		try:
			account = userdb.get_user_by_screen_name(self.current_user)
			if account:
				response = urllib2.urlopen(link, urllib.urlencode(data))
				#  access_token should look like access_token=111122828977539|98f28d8b5b8ed787b585e69b.1-537252399|1bKwe6ghzXyS9vPDyeB9b1fHLRc
				user_data = json.loads(response.read())
				account['yammer_access_token'] = user_data['access_token']
				# refresh the user token details
				#account['disqus_username'] = user_data['username']
				#account['disqus_user_id'] = user_data['user_id']
				#account['disqus_access_token'] = user_data['access_token']
				##account['disqus_expires_in'] = user_data['expires_in']
				#account['disqus_refresh_token'] = user_data['refresh_token']
				#account['disqus_token_type'] = user_data['token_type']
				userdb.save_user(account)

		except Exception, e:
			logging.info(e)
			# trouble logging in
			data = {}
		self.redirect('/user/%s/settings?msg=updated' % self.current_user)

class Remove(app.basic.BaseHandler):
	@tornado.web.authenticated
	def get(self):
		# remove twitter from this account
		account = userdb.get_user_by_screen_name(self.current_user)
		if account:
			del account['yammer_access_token']
			userdb.save_user(account)

		self.redirect('/user/%s/settings?msg=updated' % self.current_user)