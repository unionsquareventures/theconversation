import settings
from models.user_info import UserInfo
from base import BaseHandler
from urlparse import urlparse
import tornado
import datetime as dt
import urllib

class APIHandler(BaseHandler):
    def get(self):
        if self.request.path.find('/api/user_status') == 0:
            self.user_status()
        if self.request.path.find('/api/update_comment_counts') == 0:
            self.update_comment_counts()
        
    def user_status(self):
        username = self.get_current_username()
        if username:
            if self.is_staff(username):
                return(self.write("staff"))
            elif self.is_blacklisted(username):
                return(self.is_admin("blacklisted"))
            else:
                return(self.write("user"))
        else:
            return(self.write("none")) # user is not logged in

    @tornado.web.asynchronous
    def update_comment_counts(self):
        http = tornado.httpclient.AsyncHTTPClient()
        
        request_vars = {
            'api_key': settings.disqus_public_key,
            'forum': settings.disqus_apikey,
            'thread': ['link:http://www.usv.com/posts/how-we-made-a-22556-product-video']
        }
        base_url = "https://disqus.com/api/3.0/threads/set.jsonp"
        complete_url = base_url + urllib.urlencode(request_vars)
        http.fetch(complete_url, callback=self.on_disqus_response)
    
    def on_disqus_response(self, response):
        #if response.error: raise tornado.web.HTTPError(500)
        #json = tornado.escape.json_decode(response.body)
        if response:
            self.write(response.body)
        else:
            self.write('no response')
        
        self.finish()
            
            