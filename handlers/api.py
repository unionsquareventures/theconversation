from models.user_info import UserInfo
from base import BaseHandler
from urlparse import urlparse
import tornado
import datetime as dt

class APIHandler(BaseHandler):
    def get(self):
        username = self.get_current_username()
        print username
        if username:
            if self.is_staff(username):
                return(self.write("staff"))
            elif self.is_blacklisted(username):
                return(self.is_admin("blacklisted"))
            else:
                return(self.write("user"))
        else:
            return(self.write("none")) # user is not logged in



           