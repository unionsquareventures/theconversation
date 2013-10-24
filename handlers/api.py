import settings
from models.post import Post
from models.user_info import UserInfo
from base import BaseHandler
from urlparse import urlparse
import tornado
import datetime as dt
import urllib

class APIHandler(BaseHandler):
    def get(self, action=None):
        
        if self.request.path.find('/api/user_status') == 0:
            self.user_status()
            
        elif action == "update_comment_counts":
            self.refresh_comment_counts()
            
        elif action == "incr_comment_count":
            self.incr_comment_count()
            
        else:
            raise tornado.web.HTTPError(404)
      
    def post(self, action=None):
        # For some reason, I couldn't get tornado to allow me
        # to make an ajax post request.
        # kept getting a 403 error.
        # so I'm doing this by GET, and checking the referer
        
        pass
        # this will be hit by a disqus callback
        #if action == "incr_comment_count":
        #    self.incr_comment_count()
        
        #else:
        #    raise tornado.web.HTTPError(404)
        
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


    def incr_comment_count(self):
        # This will be hit by a Disqus callback,
        # coming from the Disqus JS that's on each post detail page.
        # Via an ajax request
        
        # if this isn't an ajax request coming from us, reject it
        if self.request.headers.get('Host') != settings.base_url:
            raise tornado.web.HTTPError(403)
        
        post_id = self.get_argument('post')
        comment_id = self.get_argument('comment')
        
        if not post_id or not comment_id:
            raise tornado.web.HTTPError(404)
        
        post = Post.objects(id=post_id).first()
        post.update(inc__comment_count=1)


    @tornado.web.asynchronous
    def refresh_comment_counts(self):
        # This can be called from the admin page /admin
        # and is also temporarily being hit via HTTP on a 5 min cron job
        
        http = tornado.httpclient.AsyncHTTPClient()
        
        request_vars = {
            'api_key': settings.disqus_public_key,
            'api_secret': settings.disqus_secret_key,
            'forum': settings.disqus_apikey
        }

        base_url = "https://disqus.com/api/3.0/threads/list.json"
        complete_url = base_url + "?" + urllib.urlencode(request_vars)
        http.fetch(complete_url, callback=self.on_disqus_response)
    
    def on_disqus_response(self, response):
        #if response.error: raise tornado.web.HTTPError(500)
        result = tornado.escape.json_decode(response.body)
        
        for thread in result['response']:
            self.write(thread['identifiers'][0] + " | " + thread['title'] + " | " + str(thread['posts']) + "<br />")
            post = Post.objects(id=thread['identifiers'][0]).first()
            try:
                post.update(set__comment_count=thread['posts'])
                self.write("&uarr; updated<br />")    
            except:
                self.write("&uarr; NOT updated<br />")  
                  
        #todo: loop through comments and update posts accordingly
        """
        comment_counts = {}
        for result in result['response']:
            comment_counts[result['identifiers'][0]] =  result['posts']
            self.write(result['identifiers'][0] + " | " + str(result['posts']))
        """
        self.finish()
            
            