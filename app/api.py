import app.basic
import logging
import settings

from lib import disqus
from lib import postsdb
from lib import userdb

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

