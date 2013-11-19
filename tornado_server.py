import os
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web

import logging

# settings is required/used to set our environment
import settings 

import app.user
import app.admin
import app.api
import app.basic
import app.disqus
import app.general
import app.posts
import app.redirects
import app.search
import app.twitter

class Application(tornado.web.Application):
  def __init__(self):

    debug = (tornado.options.options.environment == "dev")

    app_settings = {
      "cookie_secret" : "change_me",
      "login_url": "/",
      "debug": debug,
      "static_path" : os.path.join(os.path.dirname(__file__), "static"),
      "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    }

    handlers = [
      # redirect stuff (old links)
      (r'/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<slug>[\w\s-]+).php$', app.redirects.RedirectPosts),
      (r'/pages/.*$', app.redirects.RedirectMappings),
      (r'/team.*$', app.redirects.RedirectMappings),
      (r'/investments$', app.redirects.RedirectMappings),
      (r'/focus$', app.redirects.RedirectMappings),
    
      # account stuff
      (r"/auth/email/?", app.user.EmailSettings),
      (r"/auth/logout/?", app.user.LogOut),
      (r"/user/settings/?", app.user.UserSettings),
      (r"/user/(.+)", app.user.Profile),

      # a test line

      # admin stuff
      (r"/admin", app.admin.AdminHome),
      (r"/admin/company", app.admin.AdminCompany),
      (r"/admin/delete_user", app.admin.DeleteUser),
      (r"/admin/deleted_posts", app.admin.DeletedPosts),
      (r"/admin/sort_posts", app.admin.ReCalculateScores),
      (r"/admin/stats", app.admin.AdminStats),
      (r"/generate_hackpad/?", app.admin.GenerateNewHackpad),
      (r"/list_hackpads", app.admin.ListAllHackpad),
      (r"/posts/([^\/]+)/bumpup", app.admin.BumpUp),
      (r"/posts/([^\/]+)/bumpdown", app.admin.BumpDown),
      (r"/posts/([^\/]+)/mute", app.admin.Mute),
      (r"/users/(?P<username>[A-z-+0-9]+)/ban", app.admin.BanUser),
      (r"/users/(?P<username>[A-z-+0-9]+)/unban", app.admin.UnBanUser),

      # api stuff
      (r"/api/incr_comment_count", app.api.DisqusCallback),
      (r"/api/user_status", app.api.GetUserStatus),
      (r"/api/voted_users/(.+)", app.api.GetVotedUsers),

      # disqus stuff
      (r"/auth/disqus", app.disqus.Auth),
      (r"/remove/disqus", app.disqus.Remove),
      (r"/disqus", app.disqus.Disqus),

      # genearl site pages (and homepage)
      (r"/about", app.general.About),
      (r"/jobs", app.general.Jobs),
      (r"/network", app.general.Network),
      (r"/portfolio", app.general.Portfolio),

      # search stuff
      (r"/search", app.search.Search),
      (r"/tagged/(.+)", app.search.ViewByTag),

      # twitter stuff
      (r"/auth/twitter/?", app.twitter.Auth),
      (r"/twitter", app.twitter.Twitter),

      # post stuff
      (r"/featured.*$", app.posts.FeaturedPosts),
      (r"/feed/(?P<feed_type>[A-z-+0-9]+)$", app.posts.Feed),
      (r"/feed$", app.posts.Feed),
      (r"/posts/([^\/]+)/upvote", app.posts.UpVote),
      (r"/posts/([^\/]+)/edit", app.posts.EditPost),
      (r"/posts/(.+)", app.posts.ViewPost),
      (r"/widget.*?", app.posts.Widget),
      (r".+", app.posts.ListPosts)
    ]

    tornado.web.Application.__init__(self, handlers, **app_settings)

def main():
  tornado.options.define("port", default=8001, help="Listen on port", type=int)
  tornado.options.parse_command_line()
  logging.info("starting tornado_server on 0.0.0.0:%d" % tornado.options.options.port)
  http_server = tornado.httpserver.HTTPServer(request_callback=Application(), xheaders=True)
  http_server.listen(tornado.options.options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
