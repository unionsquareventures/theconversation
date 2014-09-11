import app.basic
import tornado.web
import settings
from datetime import datetime, date
import logging
import json
import requests

from lib import companiesdb
from lib import hackpad
from lib import postsdb
from lib import userdb
from lib import disqus
from lib import emailsdb
from disqusapi import DisqusAPI

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
                user.user.is_blacklisted = True
                user.save()
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
                screen_name = post.user.screen_name
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
            post.muted = True
            post.save()

        self.redirect('/?sort_by=hot')

###########################
### Recalc the sort socres (for hot list)
### /admin/sort_posts
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
                user.user.is_blacklisted = False
                user.save()
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