from models.post import Post
from models.user_info import UserInfo
from base import BaseHandler
from urlparse import urlparse
import tornado
import datetime as dt

class BlacklistUserHandler(BaseHandler):
    def get(self, username, action):
        if not self.is_staff(self.get_current_username()):
            raise tornado.web.HTTPError(401)
        
        if not username or not action:
            return(self.write('please supply a username and action'))
        
        author = UserInfo.objects(user__username=username).first()
        
        path = urlparse(self.request.headers.get('Referer'))[2]
        
        if action == "ban":
            author.update(set__user__is_blacklisted=True)
            #return(self.write('Author has been blacklisted'))
            self.redirect(path)    
        
        if action == "unban":
            author.update(set__user__is_blacklisted=False)
            #return(self.write('Author has been un-blacklisted'))
            self.redirect(path)