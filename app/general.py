import app.basic

from lib import postsdb

#############
### ABOUT USV
### /about
#############
class About(app.basic.BaseHandler):
    def get(self):
        # get the last 6 posts tagged thesis (and published by staff)
        related_posts = postsdb.get_latest_staff_posts_by_tag('thesis', 6)
        self.render('general/about.html', related_posts=related_posts)
