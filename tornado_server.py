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
import app.search
import app.stats
import app.twitter
import app.error
import app.redirects

class Application(tornado.web.Application):
  def __init__(self):

    debug = (settings.get('environment') == "dev")

    app_settings = {
      "cookie_secret" : "change_me",
      "login_url": "/auth/twitter",
      "debug": debug,
      "static_path" : os.path.join(os.path.dirname(__file__), "static"),
      "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    }

    handlers = [
      # redirect stuff (old links)
      # and usv-specific admin
      (r'/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<slug>[\w\s-]+).php$', app.redirects.RedirectPosts),
      (r'/pages/.*$', app.redirects.RedirectMappings),
      (r'/team.*$', app.redirects.RedirectMappings),
      (r'/investments$', app.redirects.RedirectMappings),
      (r'/focus$', app.redirects.RedirectMappings),
      (r"/admin/company", app.admin.AdminCompany),

      #general site pages
      (r"/about", app.general.About),
      (r"/jobs", app.general.Jobs),
      (r"/network", app.general.Network),
      (r"/portfolio", app.general.Portfolio),  

      # account stuff
      (r"/auth/email/?", app.user.EmailSettings),
      (r"/auth/logout/?", app.user.LogOut),
      (r"/user/settings/?", app.user.UserSettings),
      (r"/user/(.+)", app.user.Profile),

      # admin stuff
      (r"/admin", app.admin.AdminHome),
      (r"/admin/delete_user", app.admin.DeleteUser),
      (r"/admin/deleted_posts", app.admin.DeletedPosts),
      (r"/admin/sort_posts", app.admin.ReCalculateScores),
      (r"/admin/stats", app.admin.AdminStats),
      (r"/admin/disqus", app.admin.ManageDisqus),
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
      (r"/api/check_for_url", app.api.CheckForUrl),

      # disqus stuff
      (r"/auth/disqus", app.disqus.Auth),
      (r"/remove/disqus", app.disqus.Remove),
      (r"/disqus", app.disqus.Disqus),

      # search stuff
      (r"/search", app.search.Search),
      (r"/tagged/(.+)", app.search.ViewByTag),

      # stats stuff
      (r"/stats/shares/weekly", app.stats.WeeklyShareStats),

      # twitter stuff
      (r"/auth/twitter/?", app.twitter.Auth),
      (r"/twitter", app.twitter.Twitter),

      # post stuff
      (r"/featured.*$", app.posts.FeaturedPosts),
      (r"/feed/(?P<feed_type>[A-z-+0-9]+)$", app.posts.Feed),
      (r"/feed$", app.posts.Feed),
      (r"/posts/new$", app.posts.NewPost),
      (r"/bookmarklet$", app.posts.NewPost),
      (r"/(?P<sort_by>hot)$", app.posts.ListPosts),
      (r"/(?P<sort_by>new)$", app.posts.ListPosts),
      (r"/(?P<sort_by>sad)$", app.posts.ListPosts),
      (r"/(?P<sort_by>[^\/]+)/page/(?P<page>[0-9]+)$", app.posts.ListPosts),
      (r"/posts/([^\/]+)/upvote", app.posts.UpVote),
      (r"/posts/([^\/]+)/edit", app.posts.EditPost),
      (r"/posts/(.+)", app.posts.ViewPost),
      (r"/posts$", app.posts.ListPosts),
      (r"/widget/demo.*?", app.posts.WidgetDemo),
      (r"/widget.*?", app.posts.Widget),
      (r'/$', app.posts.ListPosts),
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
