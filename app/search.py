import app.basic

from lib import postsdb

class Search(app.basic.BaseHandler):
  def get(self):
    query = self.get_argument('query', '')
    tag = self.get_argument('tag', '')
    page = abs(int(self.get_argument('page', '1')))
    per_page = abs(int(self.get_argument('per_page', '10')))

    if query.strip() != '':
      # get posts based on query
      posts = postsdb.get_posts_by_query(query, per_page, page)
      total_count = postsdb.get_post_count_by_query(query)
    elif tag.strip() != '':
      posts = postsdb.get_posts_by_tag(tag, per_page, page)
      total_count = postsdb.get_post_count_by_tag(tag)

    self.render('search/search_results.html', posts=posts, total_count=total_count, page=page, per_page=per_page, query=query, tag=tag)
