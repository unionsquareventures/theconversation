import tornado.web
import app.basic

from lib import disqus
from lib import mentionsdb
from lib import postsdb
from lib import tagsdb
from lib import userdb

###########################
### EMAIL SETTINGS
### /auth/email/?
###########################
class EmailSettings(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    next_page = self.get_argument('next', '')
    subscribe_to = self.get_argument('subscribe_to', '')
    error = ''
    email = ''
    status = 'enter_email'

    # get the current user's email value
    user = userdb.get_user_by_screen_name(self.current_user)
    if user:
      email = user['email_address']

    self.render('user/email_subscribe.html', email=email, error=error, next_page=next_page, subscribe_to=subscribe_to, status=status)

  @tornado.web.authenticated
  def post(self):
    next_page = self.get_argument('next', '')
    next_page += "&finished=true"
    close_popup = self.get_argument('close_popup', '')
    email = self.get_argument('email', '')
    subscribe_to = self.get_argument('subscribe_to', '')
    error = ''
    status = ''
    slug = ''
    if close_popup != '':
      status = 'close_popup'

    # get the current user's email value
    user = userdb.get_user_by_screen_name(self.current_user)
    if user:
      # Clear the existing email address
      if email == '':
        if subscribe_to == '':
          user['email_address'] = ''
          self.set_secure_cookie('email_address', '')
          userdb.save_user(user)
          error = 'Your email address has been cleared.'
      else:
        # make sure someone else isn't already using this email
        existing = userdb.get_user_by_email(email)
        if existing and existing['user']['id_str'] != user['user']['id_str']:
          error = 'This email address is already in use.'
        else:
          # OK to save as user's email
          user['email_address'] = email
          userdb.save_user(user)
          self.set_secure_cookie('email_address', email)

          if subscribe_to != '':
            post = postsdb.get_post_by_slug(subscribe_to)
            if post:
              slug = post['slug']
              
            # Attempt to create the post's thread
            thread_id = 0
            try:
              # Attempt to create the thread.
              thread_details = disqus.create_thread(post, user['disqus_access_token'])
              thread_id = thread_details['response']['id']
            except:
              try:
                # trouble creating the thread, try to just get the thread via the slug
                thread_details = disqus.get_thread_details(slug)
                thread_id = thread_details['response']['id']
              except:
                thread_id = 0

            if thread_id != 0:
              # Subscribe a user to the thread specified in response
              disqus.subscribe_to_thread(thread_id, user['disqus_access_token'])
    
    #save email prefs
    user['wants_daily_email'] = self.get_argument('wants_daily_email', False)
    if user['wants_daily_email'] == "on":
      user['wants_daily_email'] = True
    
    user['wants_email_alerts'] = self.get_argument('wants_email_alerts', False)
    if user['wants_email_alerts'] == "on":
      user['wants_email_alerts'] = True
              
    userdb.save_user(user)
    
    self.redirect("/user/%s/settings?msg=updated" % user['user']['screen_name'])

###########################
### LOG USER OUT OF ACCOUNT
### /auth/logout
###########################
class LogOut(app.basic.BaseHandler):
  def get(self):
    self.clear_all_cookies()
    self.redirect('/')

##########################
### USER PROFILE
### /user/(.+)
##########################
class Profile(app.basic.BaseHandler):
  def get(self, screen_name, section="shares"):
    user = userdb.get_user_by_screen_name(screen_name)
    if not user:
      raise tornado.web.HTTPError(404)
    
    view = "profile"
    #section = self.get_argument('section', 'shares')
    tag = self.get_argument('tag', '')
    per_page = int(self.get_argument('per_page', 10))
    page = int(self.get_argument('page',1))
    if section == 'mentions':
      # get the @ mention list for this user
      posts = mentionsdb.get_mentions_by_user(screen_name.lower(), per_page, page)
    elif section =='bumps':
      posts = postsdb.get_posts_by_bumps(screen_name, per_page, page)
    else:
      if tag == '':
        posts = postsdb.get_posts_by_screen_name(screen_name, per_page, page)
      else:
        posts = postsdb.get_posts_by_screen_name_and_tag(screen_name, tag, per_page, page)

    # also get the list of tags this user has put in
    tags = tagsdb.get_user_tags(screen_name)

    self.render('user/profile.html', user=user, screen_name=screen_name, posts=posts, section=section, page=page, per_page=per_page, tags=tags, tag=tag, msg=None, view=view)

###########################
### USER SETTINGS
### /user/settings/?
###########################
class UserSettings(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, username=None):
    if username is None and self.current_user:
      username = self.current_user
    if username != self.current_user:
      raise tornado.web.HTTPError(401)
    
    if self.request.path.find("/user/settings") >= 0:
      self.redirect('/user/%s/settings' % username)
      
    msg = self.get_argument("msg", None)
    user = userdb.get_user_by_screen_name(self.current_user)
    if not user:
      raise tornado.web.HTTPError(404)
    
    user['wants_daily_email'] = user.get('wants_daily_email', False)
    user['wants_email_alerts'] = user.get('wants_email_alerts', True)
      
    #self.render('user/settings.html', user=user, msg=msg)
    self.render('user/profile.html', user=user, screen_name=self.current_user, posts=None, section="settings", page=None, per_page=None, tags=None, tag=None, msg=msg)
