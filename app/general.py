import app.basic
from lib import companiesdb, jobsdb, postsdb
from slugify import slugify

#############
### ABOUT USV
### /about
#############
class About(app.basic.BaseHandler):
  def get(self):
    # get the last 6 posts tagged thesis (and published by staff)
    related_posts = postsdb.get_latest_staff_posts_by_tag('thesis', 6)
    self.render('general/about.html', related_posts=related_posts)

########################
### USV & PORTFOLIO JOBS
### /jobs
########################
class Jobs(app.basic.BaseHandler):
  def get(self):
    #jobsdb.update_all() 
    jobs = jobsdb.get_all() 
    categories = jobsdb.get_categories() 
    locations = jobsdb.get_locations()
    companies = jobsdb.get_companies()
    self.render('general/jobs.html', 
      jobs=jobs, categories=categories, locations=locations, companies=companies, slugify=slugify)


###############
### USV NETWORK
### /network
###############
class Network(app.basic.BaseHandler):
  def get(self):
    # get the last 6 posts tagged usv-network (and published by staff)
    related_posts = postsdb.get_latest_staff_posts_by_tag('usv-network', 6)
    self.render('general/network.html', related_posts=related_posts)

#################
### USV PORTFOLIO
### /portfolio
#################
class Portfolio(app.basic.BaseHandler):
  def get(self):
    current = companiesdb.get_companies_by_status('current')
    exited = companiesdb.get_companies_by_status('exited')
    self.render('general/portfolio.html', current=current, exited=exited, slugify=slugify)
