import app.basic

import logging
import re
import settings
import tornado.web
import tornado.options

from datetime import datetime
from urlparse import urlparse
from lib import bitly
from lib import google
from lib import mentionsdb
from lib import postsdb
from lib import sanitize
from lib import tagsdb
from lib import userdb

###############
### EDIT A POST
### /posts/([^\/]+)/edit
###############
class EditPost(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self, slug):
    post = postsdb.get_post_by_slug(slug)
    if post and post['user']['screen_name'] == self.current_user:
      # available to edit this post
      self.render('post/edit_post.html', post=post)
    else:
      # not available to edit right now
      self.redirect('/posts/%s' % slug)

##################
### FEATURED POSTS
### /featured.*$
##################
class FeaturedPosts(app.basic.BaseHandler):
  def get(self):
    page = abs(int(self.get_argument('page', '1')))
    per_page = abs(int(self.get_argument('per_page', '9')))

    featured_posts = postsdb.get_featured_posts(per_page, page)
    total_count = postsdb.get_featured_posts_count()

    self.render('post/featured_posts.html', featured_posts=featured_posts, total_count=total_count, page=page, per_page=per_page)

##############
### FEED
### /feed
##############
class Feed(app.basic.BaseHandler):
  def get(self, feed_type="hot"):
    #action = self.get_argument('action', '')
    page = abs(int(self.get_argument('page', '1')))
    per_page = abs(int(self.get_argument('per_page', '9')))

    posts = []
    if feed_type == 'new':
      # show the newest posts
      posts = postsdb.get_new_posts(per_page, page)
    elif feed_type == 'sad':
      # show the sad posts
      posts = postsdb.get_sad_posts(per_page, page)
    else:
      # get the current hot posts
      posts = postsdb.get_hot_posts(per_page, page)

    self.render('feed.xml', posts=posts)

##############
### LIST POSTS
### /
##############
class ListPosts(app.basic.BaseHandler):
  def get(self):
    sort_by = self.get_argument('sort_by', 'hot')
    page = abs(int(self.get_argument('page', '1')))
    per_page = abs(int(self.get_argument('per_page', '20')))
    msg = ''
    featured_posts = postsdb.get_featured_posts(6, 1)
    posts = []
    is_blacklisted = False
    if self.current_user:
      is_blacklisted = self.is_blacklisted(self.current_user)
    if sort_by == 'new':
      # show the newest posts
      posts = postsdb.get_new_posts(per_page, page)
    elif sort_by == 'sad':
      # show the sad posts
      posts = postsdb.get_sad_posts(per_page, page)
    else:
      # get the current hot posts
      posts = postsdb.get_hot_posts(per_page, page)
    self.render('post/lists_posts.html', sort_by=sort_by, msg=msg, posts=posts, featured_posts=featured_posts, is_blacklisted=is_blacklisted)

  @tornado.web.authenticated
  def post(self):
    sort_by = self.get_argument('sort_by', 'hot')
    page = abs(int(self.get_argument('page', '1')))
    per_page = abs(int(self.get_argument('per_page', '9')))
    is_blacklisted = False
    msg = 'success'
    if self.current_user:
      is_blacklisted = self.is_blacklisted(self.current_user)
    post = {}
    post['title'] = unicode(self.get_argument('title', '').decode('utf-8'))
    post['url'] = self.get_argument('url', '')
    post['body_raw'] = self.get_argument('body_raw', '')
    post['tags'] = self.get_argument('tags', '').split(',')
    post['featured'] = self.get_argument('featured', '')
    post['has_hackpad'] = self.get_argument('has_hackpad', '')
    post['slug'] = self.get_argument('slug', '')
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

        long_url = post['url']
        if long_url.find('goo.gl') > -1:
          long_url = google.expand_url(post['url'])
        if long_url.find('bit.ly') > -1 or long_url.find('bitly.com') > -1:
          long_url = bitly.expand_url(post['url'].replace('http://bitly.com','').replace('http://bit.ly',''))
        post['domain'] = urlparse(long_url).netloc

      if len(posts) == 0 or bypass_dup_check != '':
        # Handle tags
        post['tags'] = [t.strip().lower() for t in post['tags']]
        post['tags'] = [t for t in post['tags'] if t]
        userdb.add_tags_to_user(self.current_user, post['tags'])
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

        user = userdb.get_user_by_screen_name(self.current_user)
        post['date_created'] = datetime.now()
        post['user_id_str'] = user['user']['id_str']
        post['username'] = self.current_user
        post['user'] = user['user']
        post['votes'] = 1
        post['voted_users'] = [user['user']]
        post['muted'] = False
        post['comment_count'] = 0
        post['disqus_thread_id_str'] = ''
        post['sort_score'] = 0.0
        post['downvotes'] = 0
        post['hackpad_url'] = ''
        post['disqus_shortname'] = settings.get('disqus_short_code')

        if post['slug'] == '':
          # save the post details
          post['slug'] = postsdb.insert_post(post)
          msg = 'success'
        else:
          # attempt to edit the post (make sure they are the author)
          saved_post = postsdb.get_post_by_slug(post['slug'])
          if saved_post and self.current_user == saved_post['user']['screen_name']:
            # looks good - let's update the saved_post values to new values
            for key in post.keys():
              saved_post[key] = post[key]
            # finally let's save the updates
            postsdb.save_post(saved_post)
            msg = 'success'

        # log any @ mentions in the post
        mentions = re.findall(r'@([^\s]+)', post['body_raw'])
        for mention in mentions:
          mentionsdb.add_mention(mention.lower(), post['slug'])

    # Send email to USVers if OP is USV
    if self.current_user in settings.get('staff') and tornado.options.options.environment == 'prod':
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

    featured_posts = postsdb.get_featured_posts(6, 1)

    if bypass_dup_check == '' and posts:
      # we should have duplicate list of posts already from above
      posts = posts
    elif sort_by == 'new':
      # show the newest posts
      posts = postsdb.get_new_posts(per_page, page)
    elif sort_by == 'sad':
      # show the sad posts
      posts = postsdb.get_sad_posts(per_page, page)
    else:
      # get the current hot posts
      posts = postsdb.get_hot_posts(per_page, page)

    self.render('post/lists_posts.html', sort_by=sort_by, msg=msg, posts=posts, featured_posts=featured_posts, is_blacklisted=is_blacklisted)

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
    subscribe = self.get_argument('subscribe', '')
    if subscribe != '':
      show_subscribe_modal = True
    else:
      show_subscribe_modal = False
    email = ''
    post = postsdb.get_post_by_slug(slug)
    if self.current_user:
      user = userdb.get_user_by_screen_name(self.current_user)
      if user:
        email = user['email_address']

      self.render('post/view_post.html', post=post, subscribe=False, email=email, show_subscribe_modal=show_subscribe_modal)
    else:
      # couldn't find a post; bounce to list
      self.redirect('/')

#############
### WIDGET
### /widget.*?
#############
class Widget(app.basic.BaseHandler):
  def get(self, extra_path=''):
    if extra_path != '':
      self.render('post/widget_demo.html')
    else:
      # list posts
      #action = self.get_argument('action', '')
      page = abs(int(self.get_argument('page', '1')))
      per_page = abs(int(self.get_argument('per_page', '9')))

      # get the current hot posts
      posts = postsdb.get_hot_posts(per_page, page)
      self.render('post/widget.js', posts=posts)
