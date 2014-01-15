import tweepy
import app.basic
import settings

from lib import userdb

####################
### AUTH VIA TWITTER
### /auth/twitter
####################
class Auth(app.basic.BaseHandler):
  def get(self):
    consumer_key = settings.get('twitter_consumer_key')
    consumer_secret = settings.get('twitter_consumer_secret')
    callback_host = 'http://%s/twitter' % self.request.headers['host']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_host, secure=True)
    auth_url = auth.get_authorization_url(True)
    self.set_secure_cookie("request_token_key", auth.request_token.key)
    self.set_secure_cookie("request_token_secret", auth.request_token.secret)
    self.redirect(auth_url)

##############################
### RESPONSE FROM TWITTER AUTH
### /twitter
##############################
class Twitter(app.basic.BaseHandler):
  def get(self):
    oauth_verifier = self.get_argument('oauth_verifier', '')
    consumer_key = settings.get('twitter_consumer_key')
    consumer_secret = settings.get('twitter_consumer_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
    auth.set_request_token(self.get_secure_cookie('request_token_key'), self.get_secure_cookie('request_token_secret'))
    auth.get_access_token(oauth_verifier)
    screen_name = auth.get_username()
    bounce_to = '/'

    access_token = {
      'secret': auth.access_token.secret,
      'user_id': '',
      'screen_name': '',
      'key': auth.access_token.key
    }

    # check if we have this user already or not in the system
    user = userdb.get_user_by_screen_name(screen_name)
    if user:
      # set the cookies based on account details
      self.set_secure_cookie("user_id_str", user['user']['id_str'])
      self.set_secure_cookie("username", user['user']['screen_name'])
      if 'email_address' not in user or ('email_address' in user and user['email_address'] == ''):
        bounce_to = '/user/%s/settings?1' % screen_name
    else:
      # need to create the account (so get more details from Twitter)
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
      api = tweepy.API(auth)
      user = api.get_user(screen_name)
      access_token['user_id'] = user.id
      access_token['screen_name'] = user.screen_name
      user_data = {
        'auth_type': 'twitter',
        'id_str': user.id_str,
        'username': user.screen_name,
        'fullname': user.name,
        'screen_name': user.screen_name,
        'profile_image_url': user.profile_image_url,
        'profile_image_url_https': user.profile_image_url_https,
      }
      # now save to mongo
      userdb.create_new_user(user_data, access_token)
      # and set our cookies
      self.set_secure_cookie("user_id_str", user.id_str)
      self.set_secure_cookie("username", user.screen_name)
      bounce_to = '/user/%s/settings?msg=twitter-thanks' % screen_name

    # let's save the screen_name to a cookie as well so we can use it for restricted bounces if need be
    self.set_secure_cookie('screen_name', screen_name, expires_days=30)

    # bounce to account
    self.redirect(bounce_to)
