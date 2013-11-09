import app.basic

from lib import companiesdb
from lib import postsdb

class About(app.basic.BaseHandler):
  def get(self):
    # get the last 6 posts tagged thesis (and published by staff)
    related_posts = postsdb.get_latest_staff_posts_by_tag('thesis', 6)
    self.render('page/about.html', related_posts=related_posts)

class Homepage(app.basic.BaseHandler):
  def get(self):
    sort_by = self.get_argument('sort_by', '')
    msg = ''
    featured_posts = []
    posts = []
    new_post = {}
    self.render('post/index.html', sort_by=sort_by, msg=msg, new_post=new_post, posts=posts, featured_posts=featured_posts)

class Jobs(app.basic.BaseHandler):
  def get(self):
    self.render('page/jobs.html')

class Network(app.basic.BaseHandler):
  def get(self):
    # get the last 6 posts tagged usv-network (and published by staff)
    related_posts = postsdb.get_latest_staff_posts_by_tag('usv-network', 6)
    self.render('page/network.html', related_posts=related_posts)

class Portfolio(app.basic.BaseHandler):
  def get(self):
    current = companiesdb.get_companies_by_status('current')
    exited = companiesdb.get_companies_by_status('exited')
    slugify = ''
    self.render('page/portfolio.html', current=current, exited=exited, slugify=slugify)
