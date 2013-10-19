import settings
from models.post import Post
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
        
        threads = [
            'link:http://www.usv.com/posts/how-we-made-a-22556-product-video',
            'link:http://www.usv.com/posts/pay-heed-to-the-internets-third-wave-cows-of-disruption'
        ]
        
        request_vars = {
            'api_key': settings.disqus_public_key,
            'api_secret': settings.disqus_secret_key,
            'forum': settings.disqus_apikey
        }

        #thread_string = "&" + urllib.urlencode(thread)ing += urllib.urlencode(thread)
        
        #thread_string = "&thread[]=" + "&thread[]=".join(threads)
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
            
            