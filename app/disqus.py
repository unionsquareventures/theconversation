import urllib2
import urllib
import simplejson as json
import tornado.web
import logging
import settings
import app.basic
from datetime import datetime

from lib import userdb
from lib import postsdb
from lib import disqus

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
                disqus_obj = {}
                disqus_obj['username'] = user_data['username']
                disqus_obj['user_id'] = user_data['user_id']
                disqus_obj['access_token'] = user_data['access_token']
                disqus_obj['expires_in'] = user_data['expires_in']
                disqus_obj['refresh_token'] = user_data['refresh_token']
                disqus_obj['token_type'] = user_data['token_type']
                disqus_obj['token_startdate'] = datetime.now()
                account['disqus'] = disqus_obj
                if 'disqus_username' in account.keys(): del account['disqus_username']
                if 'disqus_user_id' in account.keys(): del account['disqus_user_id']
                if 'disqus_access_token' in account.keys(): del account['disqus_access_token']
                if 'disqus_expires_in' in account.keys(): del account['disqus_expires_in']
                if 'disqus_refresh_token' in account.keys(): del account['disqus_refresh_token']
                if 'disqus_token_type' in account.keys(): del account['disqus_token_type']
                userdb.save_user(account)

                # subscribe user to all previous threads they've written
                disqus.subscribe_to_all_your_threads(self.current_user)

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
            del account['disqus']
            userdb.save_user(account)

        self.redirect('/user/%s/settings?msg=updated' % self.current_user)
