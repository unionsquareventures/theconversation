import urllib2
import urllib
import simplejson as json
import tornado.web

import settings
import app.basic

from lib import userdb

class Auth(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    req_host = self.request.headers['host']
    client_id = settings.get('disqus_public_key')
    redirect_url = 'https://disqus.com/api/oauth/2.0/authorize/?client_id=%s&scope=read,write&response_type=code&redirect_uri=http://%s/disqus'  % (client_id, req_host)
    self.redirect(redirect_url)

class Disqus(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    code = self.get_argument('code','')
    req_host = self.request.headers['host']
    api_key = settings.get('disqus_public_key')
    api_secret = settings.get('disqus_secret_key')

    link = 'https://disqus.com/api/oauth/2.0/access_token/'
    data = {
      'grant_type':'authorization_code',
      'client_id':api_key,
      'client_secret':api_secret,
      'redirect_uri': 'http://%s/disqus' % req_host,
      'code' : code
    }
    try:
      account = userdb.get_user_by_screen_name(self.current_user)
      if account:
        response = urllib2.urlopen(link, urllib.urlencode(data))
        #  access_token should look like access_token=111122828977539|98f28d8b5b8ed787b585e69b.1-537252399|1bKwe6ghzXyS9vPDyeB9b1fHLRc
        user_data = json.loads(response.read())
        # refresh the user token details
        account['disqus_username'] = user_data['username']
        account['disqus_user_id'] = user_data['user_id']
        account['disqus_access_token'] = user_data['access_token']
        account['disqus_expires_in'] = user_data['expires_in']
        account['disqus_refresh_token'] = user_data['refresh_token']
        account['disqus_token_type'] = user_data['token_type']
        userdb.save_user(account)
    except:
      # trouble logging in
      data = {}
    self.redirect('/user/settings?section=social_accounts')

class Remove(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    # remove twitter from this account
    account = userdb.get_user_by_screen_name(self.current_user)
    if account:
      del account['disqus_username']
      del account['disqus_user_id']
      del account['disqus_access_token']
      del account['disqus_expires_in']
      del account['disqus_refresh_token']
      del account['disqus_token_type']
      userdb.save_user(account)

    self.redirect('/user/settings?section=social_accounts')
