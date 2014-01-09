import app.basic
import tornado.web
import settings
import datetime
import logging
import json
import re, time, imaplib
import requests

from lib import companiesdb, postsdb, userdb, gmaildb
from lib import hackpad
from lib import disqus
from lib import emailsdb
from disqusapi import DisqusAPI

############################
# ADMIN NEWSLETTER
# /admin/newsletter
############################
class DailyEmail(app.basic.BaseHandler):
  def get(self):
    posts = postsdb.get_hot_posts()
    has_previewed = self.get_argument("preview", False)
    #on this page, you'll choose from hot posts and POST the selections to the email form`
    self.render('admin/daily_email.html', posts=posts, slugs=None, email=None, has_previewed=has_previewed, has_sent=False)
  
  def post(self):
    if not self.current_user_can('send_daily_email'):
      raise tornado.web.HTTPError(401)
    
    slugs = self.request.arguments['slugs']
    if not slugs:
      return self.write("No posts selected")
    
    email = emailsdb.construct_daily_email(slugs)
   
    if self.get_argument('preview', '') == "true":
      self.render('admin/daily_email.html', slugs=slugs, posts=None, email=email, has_previewed=True, has_sent=False)
    else:
      emailsdb.send_daily_email(email)
      self.redirect('/admin/daily_email/history')

class DailyEmailHistory(app.basic.BaseHandler):
  def get(self):
    history = emailsdb.get_daily_email_log()
    self.render('admin/daily_email_history.html', history=history)
    
    
###########################
### ADMIN COMPANY
### /admin/company
###########################
class AdminCompany(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      slug = self.get_argument('slug', '')

      company = {
        'id':'', 'name':'', 'url':'', 'description':'', 'logo_filename':'',
        'locations':'', 'investment_series':'', 'investment_year':'', 'categories':'',
        'satus':'', 'slug':'', 'investment_post_slug':''
      }
      if slug != '':
        company = companiesdb.get_company_by_slug(slug)
        if not company:
          company = {
            'id':'', 'name':'', 'url':'', 'description':'', 'logo_filename':'',
            'locations':'', 'investment_series':'', 'investment_year':'', 'categories':'',
            'satus':'', 'slug':'', 'investment_post_slug':''
          }

      self.render('admin/admin_company.html', company=company)

  @tornado.web.authenticated
  def post(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      company = {}
      company['id'] = self.get_argument('id', '')
      company['name'] = self.get_argument('name', '')
      company['url'] = self.get_argument('url', '')
      company['description'] = self.get_argument('description', '')
      company['logo_filename'] = self.get_argument('logo_filename', '')
      company['locations'] = self.get_argument('locations', '')
      company['investment_series'] = self.get_argument('investment_series', '')
      company['investment_year'] = self.get_argument('investment_year', '')
      company['categories'] = self.get_argument('categories', '')
      company['status'] = self.get_argument('status', '')
      company['slug'] = self.get_argument('slug', '')
      company['investment_post_slug'] = self.get_argument('investment_post_slug', '')

      # save the company details
      companiesdb.save_company(company)

      self.render('admin/admin_company.html', company=company)

###########################
### List the available admin tools
### /admin
###########################
class AdminHome(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      self.render('admin/admin_home.html')

###########################
### View system statistics
### /admin/stats
###########################
class AdminStats(app.basic.BaseHandler):
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      total_posts = postsdb.get_post_count()
      total_users = userdb.get_user_count()

    self.render('admin/admin_stats.html', total_posts=total_posts, total_users=total_users)

###########################
### Add a user to the blacklist
### /users/(?P<username>[A-z-+0-9]+)/ban
###########################
class BanUser(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, screen_name):
    if self.current_user in settings.get('staff'):
      user = userdb.get_user_by_screen_name(screen_name)
      if user:
        user['user']['is_blacklisted'] = True
        userdb.save_user(user)
    self.redirect('/')

###########################
### List posts that are marekd as deleted
### /admin/delete_user
###########################
class DeletedPosts(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if not self.current_user_can('delete_posts'):
      self.redirect('/')
    else:
      page = abs(int(self.get_argument('page', '1')))
      per_page = abs(int(self.get_argument('per_page', '10')))

      deleted_posts = postsdb.get_deleted_posts(per_page, page)
      total_count = postsdb.get_deleted_posts_count()

      self.render('admin/deleted_posts.html', deleted_posts=deleted_posts, total_count=total_count, page=page, per_page=per_page)

###########################
### Mark all shares by a user as 'deleted'
### /admin/deleted_posts
###########################
class DeleteUser(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if not self.current_user_can('delete_users'):
      self.redirect('/')
    else:
      msg = self.get_argument('msg', '')
      self.render('admin/delete_user.html', msg=msg)

  @tornado.web.authenticated
  def post(self):
    if not self.current_user_can('delete_users'):
      self.redirect('/')
    else:
      msg = self.get_argument('msg', '')
      post_slug = self.get_argument('post_slug', '')
      post = postsdb.get_post_by_slug(post_slug)
      if post:
        # get the author of this post
        screen_name = post['user']['screen_name']
        postsdb.delete_all_posts_by_user(screen_name)
      self.ender('admin/delete_user.html', msg=msg)

###########################
### Create a new hackpad
### /generate_hackpad/?
###########################
class GenerateNewHackpad(app.basic.BaseHandler):
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      hackpads = hackpad.create_hackpad()
      self.api_response(hackpads)

###########################
### List all hackpads
### /list_hackpads
###########################
class ListAllHackpad(app.basic.BaseHandler):
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      hackpads = hackpad.list_all()
      self.api_response(hackpads)

###########################
### Mute (hide) a post
### /posts/([^\/]+)/mute
###########################
class Mute(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, slug):
    post = postsdb.get_post_by_slug(slug)

    if post and self.current_user_can('mute_posts'):
      post['muted'] = True
      postsdb.save_post(post)

    self.redirect('/?sort_by=hot')

###########################
### Recalc the sort socres (for hot list)
### /admin/sort_posts
### Now redundant with scripts/sort_posts.py
###########################
class ReCalculateScores(app.basic.BaseHandler):
  def get(self):
    postsdb.sort_posts()
    self.redirect('/')

###########################
### Remove user from blacklist
### /users/(?P<username>[A-z-+0-9]+)/unban
###########################
class UnBanUser(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, screen_name):
    if self.current_user in settings.get('staff'):
      user = userdb.get_user_by_screen_name(screen_name)
      if user:
        user['user']['is_blacklisted'] = False
        userdb.save_user(user)
    self.redirect('/')

###########################
### Manage Disqus Data
### /admin/disqus
###########################
class ManageDisqus(app.basic.BaseHandler):
  def get(self):
    if not self.current_user_can('manage_disqus'):
      return self.write("not authorized")
    
    from disqusapi import DisqusAPI
    disqus = DisqusAPI(settings.get('disqus_secret_key'), settings.get('disqus_public_key'))
    for result in disqus.trends.listThreads():
        self.write(result)
    #response = disqus.get_all_threads()
    #self.write(response)

###########################
### Manage Disqus Data
### /admin/gmail
###########################
class Gmail(app.basic.BaseHandler):
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')

    query = self.get_argument('q', '')
    if not query:
      correspondences = []
    else:
      # Query each account
      accounts = gmaildb.get_all()
      print "accounts"
      print accounts
      correspondences = []
      for usv_member in accounts:
        mail = self.email_login(usv_member['account'], usv_member['password'])
        if mail:
          total_emails_in, recent_email_in = self.search_mail(mail, "FROM " + query)
          total_emails_out, recent_email_out = self.search_mail(mail, "TO " + query)
          correspondence = {'usv_member': usv_member['account'], 'total_emails_in': total_emails_in, 'total_emails_out': total_emails_out, 'recent_email_in': recent_email_in, 'recent_email_out': recent_email_out}
          correspondences.append(correspondence)

    return self.render('admin/gmail.html', correspondences=correspondences, query=query)

  ''' Simple query to the inbox, returns how many emails match query and the date of the latest email.
      Query must be a single string, i.e. not "science exchange" '''
  def search_mail(self, mail, query):
      if not query:
        query = "ALL"
      result, data = mail.search(None, query) # data is a list, but there is only data[0]. data[0] is a string of all the email ids for the given query. ex: ['1 2 4']
      ids = data[0] # ids is a space separated string containing all the ids of email messages
      id_list = ids.split() # id_list is an array of all the ids of email messages

      # Get date of latest email
      if id_list:
        latest_id = id_list[-1]
        result, data = mail.fetch(latest_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        raw_email = data[0][1] # raw_email is the body, i.e. the raw text of the whole email including headers and alternate payloads     
        date = self.get_mail_date(raw_email)
      else:
        date = None
      return len(id_list), date

  ''' Login into an account '''
  def email_login(self, account, password):
    try:
      mail = imaplib.IMAP4_SSL('imap.gmail.com')
      result, message = mail.login(account, password)
      mail.select("[Gmail]/All Mail", readonly=True) #mark as unread 
      if result != 'OK':
        raise Exception
      print 'Logged in as ' + account
      return mail
    except:
      print "Failed to log into " + account
      return None

  ''' Parses raw email and returns date sent. Picks out dates of the form "26 Aug 2013" '''
  def get_mail_date(self, raw_email):
    if raw_email:
      #Date: Mon, 5 Nov 2012 17:45:38 -0500
      date_string = re.search(r'[0-3]*[0-9] [A-Z][a-z][a-z] 20[0-9][0-9]', raw_email)
      if date_string:
        time_obj = time.strptime(date_string.group(), "%d %b %Y")
        return datetime.date(time_obj.tm_year, time_obj.tm_mon, time_obj.tm_mday)
      else:
        return None
    else:
      raise Exception


