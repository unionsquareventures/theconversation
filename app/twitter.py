import tweepy
import app.basic
import settings

class Auth(app.basic.BaseHandler):
  def get(self):
    consumer_key = settings.get('consumer_key')
    consumer_secret = settings.get('consumer_secret')
    callback_host = 'http://%s/twitter' % self.request.headers['host']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_host)
    auth_url = auth.get_authorization_url(True)
    self.set_secure_cookie("request_token_key", auth.request_token.key)
    self.set_secure_cookie("request_token_secret", auth.request_token.secret)
    self.redirect(auth_url)

class Twitter(app.basic.BaseHandler):
  def get(self):
    oauth_verifier = self.get_argument('oauth_verifier', '')
    consumer_key = settings.get('consumer_key')
    consumer_secret = settings.get('consumer_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_request_token(self.get_secure_cookie('request_token_key'), self.get_secure_cookie('request_token_secret'))
    auth.get_access_token(oauth_verifier)
    screen_name = auth.get_username()

    access_token = {
      'secret': auth.access_token.secret,
      'user_id': '',
      'screen_name': '',
      'key': auth.access_token.key
    }

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
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

    # let's save the screen_name to a cookie as well so we can use it for restricted bounces if need be
    self.set_secure_cookie('screen_name', screen_name, expires_days=30)
    if not self.current_user:
      # attempt to log user in (or create account)
      self.set_secure_cookie("user_id_str", user.id_str)
      self.set_secure_cookie("username", user.screen_name)

    # bounce to account
    self.redirect('/')
