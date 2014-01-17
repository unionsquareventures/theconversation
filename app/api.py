import app.basic
import logging
import settings
import datetime

from lib import disqus
from lib import postsdb
from lib import userdb

#########################
### Alerting to share owner (and other subscribers) on new Disqus comments
### /api/incr_comment_count
#########################
class DisqusCallback(app.basic.BaseHandler):
  def get(self):
    comment = self.get_argument('comment', '')
    post_slug = self.get_argument('post', '')
    post = postsdb.get_post_by_slug(post_slug)

    if post:
      # increment the comment count for this post
      post['comment_count'] += 1
      postsdb.save_post(post)
      # determine if anyone is subscribed to this post (for email alerts)
      if len(post['subscribed']) > 0:
        # attempt to get the current user's email (we don't need to alert them)
        author_email = ''
        if self.current_user:
          author = userdb.get_user_by_screen_name(self.current_user)
          if author and 'email_address' in author.keys() and author['email_address'].strip() != '':
            author_email = author['email_address']
        # get the message details from Disqus
        message = disqus.get_post_details(comment)
        if message['message'].strip() != '':
          # send the emails with details
          logging.info(message)
          subject = 'New message on: %s' % post['title']
          text = 'The following comment was just added to your share on usv.com.\n\n%s\n\nYou can engaged in the conversation, and manage your alert settings for this share, at http://www.usv.com/posts/%s' % (message['message'], post['slug'])
          for email in post['subscribed']:
            # attempt to send to each of these subscribed people (don't send to author)
            if email.lower() != author_email.lower() and email.strip() != '':
              self.send_email('alerts@usv.com', email, subject, text)
    self.api_response('OK')

#########################
### Get a user's status
### /api/user_status
#########################
class GetUserStatus(app.basic.BaseHandler):
  def get(self):
    status = 'none'
    if self.current_user:
      if self.current_user in settings.get('staff'):
        status = 'staff'
      elif self.is_blacklisted(self.current_user):
        status = 'blacklisted'
      else:
        status = 'user'
    self.api_response(status)

#########################
### Get list of users who have voted on a post
### /api/voted_users/(.+)
#########################
class GetVotedUsers(app.basic.BaseHandler):
  def get(self, slug):
    voted_users = []
    post = postsdb.get_post_by_slug(slug)
    if post:
      voted_users = post['voted_users']
      for user in voted_users:
        if user.get('username') == post['user']['username']:
          voted_users.remove(user)
      self.render('post/voted_users.html', voted_users=voted_users)
    
#########################
### Check to see if we already have a post by url
### /api/check_for_url?url=foo
#########################
class CheckForUrl(app.basic.BaseHandler):
  def get(self, url):
    response = {
      "exists": False,
      "posts": []
    }
    posts = postsdb.get_post_by_url(url)
    if len(posts) > 0:
      response["exists"] = True
      response["posts"] = posts
    self.api_response(response)

############################
### Get a day's worth of posts
### /api/posts/get_day
############################
class PostsGetDay(app.basic.BaseHandler):
  def get(self):
    day = datetime.datetime.strptime(self.get_argument('day'), "%a, %d %b %Y %H:%M:%S %Z")
    yesterday = day - datetime.timedelta(days=1)
    posts = postsdb.get_hot_posts_by_day(day)
    html = self.render_string('post/daily_posts_list_snippet.html', today=day, yesterday=yesterday, posts=posts, current_user_can=self.current_user_can)
    response = {}
    response['html'] = html
    self.api_response(response)
