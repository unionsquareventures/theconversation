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
    jobs = jobsdb.get_all() 
    categories = jobsdb.get_categories() 
    locations = jobsdb.get_locations()
    companies = jobsdb.get_companies()
    self.render('general/jobs.html', 
      jobs=jobs, categories=categories, locations=locations, companies=companies, slugify=slugify)

#################
### USV PORTFOLIO
### /portfolio
#################
class Portfolio(app.basic.BaseHandler):
  def get(self):
    current = companiesdb.get_companies_by_status('current')
    exited = companiesdb.get_companies_by_status('exited')
    self.render('general/portfolio.html', current=current, exited=exited, slugify=slugify)

#################
### Hangouts
### /hangoutwith/()
#################
class Hangouts(app.basic.BaseHandler):
  def get(self, who=None):
    if who not in ["everyone", "fred", "brad", "albert", "john", "andy", "brittany", "brian", "zander", "nick"]:
      return(self.write('no hangout specified'))
    if who == "everyone":
      self.redirect("https://plus.google.com/hangouts/_/event/csjrctgcaphdptmqacnfisq0i2g")
    elif who == "fred":
      self.redirect("https://plus.google.com/hangouts/_/event/cis1kcq11fkqlj12egf0pu74tlc")
    elif who == "andy":
      self.redirect("https://plus.google.com/hangouts/_/event/coak3i6919ch7m9dvlq50no4smo")
    elif who == "albert":
      self.redirect("https://plus.google.com/hangouts/_/event/cdhdic31990mu30tmdbec3ucbos")
    elif who == "brad":
      self.redirect("https://plus.google.com/hangouts/_/event/cq29i1aohb1abtc1qs8fpgstrio")
    
