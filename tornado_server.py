import os
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web

import logging

# settings is required/used to set our environment
import settings 

import app.account
import app.basic
import app.general
import app.posts
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
      # twitter stuff
      (r'/auth/twitter/?', app.twitter.Auth),
      (r'/twitter', app.twitter.Twitter),
      (r'/auth/logout/?', app.account.LogOut),

      # search stuff
      (r"/search", app.search.Search),
      (r"/tagged/(.+)", app.search.ViewByTag),

      # genearl site pages (and homepage)
      (r"/about", app.general.About),
      (r"/jobs", app.general.Jobs),
      (r"/network", app.general.Network),
      (r"/portfolio", app.general.Portfolio),

      # post stuff
      (r"/posts/([^\/]+)/upvote", app.posts.UpVote),
      (r"/posts/(.+)", app.posts.ViewPost),
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
