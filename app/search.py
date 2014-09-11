import app.basic
import urllib

from lib import postsdb
from lib import tagsdb

################
### SEARCH POSTS
### /search
################
class Search(app.basic.BaseHandler):
    def get(self):
        query = self.get_argument('query', '')
        page = abs(int(self.get_argument('page', '1')))
        per_page = abs(int(self.get_argument('per_page', '10000')))

        # get posts based on query
        posts = postsdb.get_posts_by_query(query, per_page, page)
        total_count = postsdb.get_post_count_by_query(query)
        tags_alpha = tagsdb.get_all_tags(sort="alpha")
        tags_count = tagsdb.get_all_tags(sort="count")
        tag = ""

        self.render('search/search_results.html', posts=posts, tag=tag, tags_alpha=tags_alpha, tags_count=tags_count, total_count=total_count, page=page, per_page=per_page, query=query)

#####################
### VIEW POSTS BY TAG
### /tagged/(.+)
#####################
class ViewByTag(app.basic.BaseHandler):
    def get(self, tag=None):
        if tag:
            tag = urllib.unquote(tag.strip().replace('+',' ')).decode('utf8')
            posts = postsdb.get_posts_by_tag(tag)
            total_count = postsdb.get_post_count_by_tag(tag)
        else:
            posts = None
            total_count = 0

        featured_posts = postsdb.get_featured_posts(5, 1)
        tags_alpha = tagsdb.get_all_tags(sort="alpha")
        tags_count = tagsdb.get_all_tags(sort="count")

        self.render('search/search_results.html', tag=tag, tags_alpha=tags_alpha, tags_count=tags_count, posts=posts, total_count=total_count, query=tag)
