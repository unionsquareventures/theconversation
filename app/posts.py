import app.basic

import logging
import settings
import tornado.web
import tornado.options

from datetime import datetime
from urlparse import urlparse
from lib import userdb
from lib import postsdb
from lib import sanitize
from lib import tagsdb

##############
### LIST POSTS
### /
##############
class ListPosts(app.basic.BaseHandler):
  def get(self):
    sort_by = self.get_argument('sort_by', 'hot')
    msg = ''
    featured_posts = postsdb.get_featured_posts(6)
    posts = []
    if sort_by == 'new':
      # show the newest posts
      posts = postsdb.get_new_posts()
    elif sort_by == 'sad':
      # show the sad posts
      posts = postsdb.get_sad_posts()
    else:
      # get the current hot posts
      posts = postsdb.get_hot_posts()
    new_post = {}
    self.render('post/lists_posts.html', sort_by=sort_by, msg=msg, new_post=new_post, posts=posts, featured_posts=featured_posts)

  @tornado.web.authenticated
  def post(self):
    sort_by = self.get_argument('sort_by', 'hot')
    post = {}
    post['title'] = unicode(self.get_argument('title', '').decode('utf-8'))
    post['url'] = self.get_argument('url', '')
    post['body_raw'] = self.get_argument('body_raw', '')
    post['tags'] = self.get_argument('tags', '').split(',')
    post['featured'] = self.get_argument('featured', '')
    post['has_hackpad'] = self.get_argument('has_hackpad', '')
    if post['has_hackpad'] != '':
      post['has_hackpad'] = True
    else:
      post['has_hackpad'] = False

    deleted = self.get_argument('deleted', '')
    if deleted != '':
      post['deleted'] = True
      post['date_deleted'] = datetime.now()

    bypass_dup_check = self.get_argument('bypass_dup_check', '')
    posts = []

    # make sure user isn't blacklisted
    if not self.is_blacklisted(self.current_user):
      # check if there is an existing URL
      if post['url'] != '':
        url = urlparse(post['url'])
        netloc = url.netloc.split('.')
        if netloc[0] == 'www':
          del netloc[0]
        path = url.path
        if path and path[-1] == '/':
          path = path[:-1]
        url = '%s%s' % ('.'.join(netloc), path)
        post['normalized_url'] = url
        posts = postsdb.get_posts_by_normalized_url(post['normalized_url'], 5)

      if len(posts) == 0 or bypass_dup_check != '':
        # Handle tags
        post['tags'] = [t.strip().lower() for t in post['tags']]
        post['tags'] = [t for t in post['tags'] if t]
        for tag in post['tags']:
          tagsdb.save_tag(tag)

        # format the content as needed
        post['body_html'] = sanitize.html_sanitize(post['body_raw'], media=self.current_user_can('post_rich_media'))
        post['body_text'] = sanitize.html_to_text(post['body_html'])
        post['body_truncated'] = sanitize.truncate(post['body_text'], 500)

        # determine if this should be a featured post or not
        if self.current_user_can('feature_posts') and post['featured'] != '':
          post['featured'] = True
          post['date_featured'] = datetime.now()
        else:
          post['featured'] = False
          post['date_featured'] = None

        account = userdb.get_user_by_screen_name(self.current_user)
        post['date_created'] = datetime.now()
        post['user_id_str'] = account['user']['id_str']
        post['username'] = self.current_user
        post['user'] = account['user']
        post['votes'] = 1
        post['voted_users'] = [account['user']]
        post['muted'] = False
        post['comment_count'] = 0
        post['disqus_thread_id_str'] = ''
        post['sort_score'] = 0.0
        post['downvotes'] = 0
        post['hackpad_url'] = ''
        post['disqus_shortname'] = 'usvbeta2'

        # save the post details
        postsdb.insert_post(post)

    """
    # Send email to USVers if OP is USV
    if self.get_current_user_role() == 'staff' and tornado.options.options.environment == 'prod':
      subject = 'USV.com: %s posted "%s"' % (post.user['username'], post.title)
      if post.url: # post.url is the link to external content (if any)
        post_link = 'External Link: %s \n\n' % post.url
      else:
        post_link = ''
      post_url = "http://%s/posts/%s" % (settings.base_url, post.slug)
      text = '"%s" ( %s ) posted by %s. \n\n %s %s' % (post.title.encode('ascii', errors='ignore'), post_url, post.user['username'].encode('ascii', errors='ignore'), post_link, post.body_text)
      # now attempt to actually send the emails
      for u in settings.get('staff'):
        if u != self.current_user:
          acc = userdb.get_user_by_screen_name(u)
          self.send_email('web@usv.com', acc['email_address'], subject, text)
          logging.info("Email sent to %s" % acc['email_address'])
    """

    new_post = {}
    msg = ''
    featured_posts = postsdb.get_featured_posts(6)

    if bypass_dup_check == '' and posts:
      # we should have duplicate list of posts already from above
      posts = posts
    elif sort_by == 'new':
      # show the newest posts
      posts = postsdb.get_new_posts()
    elif sort_by == 'sad':
      # show the sad posts
      posts = postsdb.get_sad_posts()
    else:
      # get the current hot posts
      posts = postsdb.get_hot_posts()

    self.render('post/lists_posts.html', sort_by=sort_by, msg=msg, new_post=new_post, posts=posts, featured_posts=featured_posts)

##########################
### UPVOTE A SPECIFIC POST
### /posts/([^\/]+)/upvote
##########################
class UpVote(app.basic.BaseHandler):
  def get(self, slug):
    # user must be logged in
    msg = {}
    if not self.current_user:
      msg = {'error': 'You must be logged in to upvote.', 'redirect': True}
    else:
      post = postsdb.get_post_by_slug(slug)
      if post:
        can_vote = True
        for u in post['voted_users']:
          if u['screen_name'] == self.current_user:
            can_vote = False
        if not can_vote and not self.current_user_can('upvote_multiple_times'):
          msg = {'error': 'You have already upvoted this post.'}
        else:
          user = userdb.get_user_by_screen_name(self.current_user)
          # Increment the vote count
          post['votes'] += 1
          post['voted_users'].append(user['user'])
          postsdb.save_post(post)
          msg = {'votes': post['votes']}

      self.api_response(msg)

########################
### VIEW A SPECIFIC POST
### /posts/(.+)
########################
class ViewPost(app.basic.BaseHandler):
  def get(self, slug):
    post = postsdb.get_post_by_slug(slug)
    user_info = {}
    if self.current_user:
      user_info = userdb.get_user_by_screen_name(self.current_user)
      self.render('post/view_post.html', post=post, disqus_sso={}, user_info=user_info, subscribe=False, author=post['user'])
