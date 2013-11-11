import app.basic
import tornado.web
import settings

from lib import postsdb

class AdminHome(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      self.render('admin/admin_home.html')

class BumpUp(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, slug):
    post = postsdb.get_post_by_slug(slug)

    #if self.current_user_can('super_upvote_posts'):
      # self.redis_incrby(post, 0.25)

    self.redirect('/?sort_by=hot')

class BumpDown(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, slug):
    post = postsdb.get_post_by_slug(slug)

    #if self.current_user_can('downvote_posts'):
      # self.redis_incrby(post, -0.25)

    self.redirect('/?sort_by=hot')

class Mute(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, slug):
    post = postsdb.get_post_by_slug(slug)

    if post and self.current_user_can('mute_posts'):
      post['muted'] = True
      postsdb.save_post(post)

    self.redirect('/?sort_by=hot')

