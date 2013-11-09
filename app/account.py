import app.basic

class EmailAuth(app.basic.BaseHandler):
  def get(self):
    self.redirect('/')

class LogOut(app.basic.BaseHandler):
  def get(self):
    self.clear_all_cookies()
    self.redirect('/')