import app.basic
import urllib

from lib import postsdb

################
### SEARCH POSTS
### /search
################
class Search(app.basic.BaseHandler):
  def get(self):
    query = self.get_argument('query', '')
    page = abs(int(self.get_argument('page', '1')))
    per_page = abs(int(self.get_argument('per_page', '10')))

    # get posts based on query
    posts = postsdb.get_posts_by_query(query, per_page, page)
    total_count = postsdb.get_post_count_by_query(query)

    self.render('search/search_results.html', posts=posts, total_count=total_count, page=page, per_page=per_page, query=query)

#####################
### VIEW POSTS BY TAG
### /tagged/(.+)
#####################
class ViewByTag(app.basic.BaseHandler):
  def get(self, tag):
    page = abs(int(self.get_argument('page', '1')))
    per_page = abs(int(self.get_argument('per_page', '10')))
    tag = urllib.unquote(tag.strip().replace('+',' ')).decode('utf8')
    posts = postsdb.get_posts_by_tag(tag, per_page, page)
    total_count = postsdb.get_post_count_by_tag(tag)
    self.render('search/search_results.html', posts=posts, total_count=total_count, page=page, per_page=per_page, query=tag)

