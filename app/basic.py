import tornado.web
import requests
import settings
import simplejson as json
import os
import httplib
import logging

from lib import userdb

class BaseHandler(tornado.web.RequestHandler):
  def __init__(self, *args, **kwargs):
    super(BaseHandler, self).__init__(*args, **kwargs)
    #user = self.get_current_user()
    #css_file = "%s/css/threatvector.css" % settings.tornado_config['static_path']
    #css_modified_time = os.path.getmtime(css_file)
      
    self.vars = {
      #'user': user,
      #'css_modified_time': css_modified_time
    }
                
  def render(self, template, **kwargs):
  
    # add any variables we want available to all templates
    kwargs['user_obj'] = None
    kwargs['user_obj'] = userdb.get_user_by_screen_name(self.current_user)
    kwargs['current_user_can'] = self.current_user_can 
    kwargs['settings'] = settings 
    kwargs['body_location_class'] = ""
    kwargs['current_path'] = self.request.uri
    #kwargs['request_path'] = self.request
    
    if self.request.path == "/":
      kwargs['body_location_class'] = "home"
  
    super(BaseHandler, self).render(template, **kwargs)
    
  def get_current_user(self):
    return self.get_secure_cookie("username")

  def send_email(self, from_user, to_user, subject, text):
    if settings.get('environment') != "prod":
      logging.info("If this were prod, we would have sent email to %s" % to_user)
      return
    else:
      return requests.post(
        "https://sendgrid.com/api/mail.send.json",
        data={
          "api_user":settings.get('sendgrid_user'),
          "api_key":settings.get('sendgrid_secret'),
          "from": from_user,
          "to": to_user,
          "subject": subject,
          "text": text
        },
        verify=False
      )
      
    
  def is_blacklisted(self, screen_name):
    u = userdb.get_user_by_screen_name(screen_name)
    if u and 'user' in u.keys() and 'is_blacklisted' in u['user'].keys() and u['user']['is_blacklisted']:
      return True
    return False

  def current_user_can(self, capability):
    """
    Tests whether a user can do a certain thing.
    """
    result = False
    u = userdb.get_user_by_screen_name(self.current_user)
    if u and 'role' in u.keys():
      try:
        if capability in settings.get('%s_capabilities' % u['role']):
          result = True
      except:
        result = False
    return result

  def api_response(self, data):
    # return an api response in the proper output format with status_code == 200
    self.write_api_response(data, 200, "OK")

  def error(self, status_code, status_txt, data=None):
    # return an api error in the proper output format
    self.write_api_response(status_code=status_code, status_txt=status_txt, data=data)

  def write_api_response(self, data, status_code, status_txt):
    # return an api error based on the appropriate request format (ie: json)
    format = self.get_argument('format', 'json')
    callback = self.get_argument('callback', None)
    if format not in ["json"]:
      status_code = 500
      status_txt = "INVALID_ARG_FORMAT"
      data = None
      format = "json"
    response = {'status_code':status_code, 'status_txt':status_txt, 'data':data}

    if format == "json":
      data = json.dumps(response)
      if callback:
        self.set_header("Content-Type", "application/javascript; charset=utf-8")
        self.write('%s(%s)' % (callback, data))
      else:
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(data)
      self.finish()
  
  def write_error(self, status_code, **kwargs):
    self.require_setting("static_path")
    if status_code in [404, 500, 503, 403]:
        filename = os.path.join(self.settings['static_path'], '%d.html' % status_code)
        if os.path.exists(filename):
            f = open(filename, 'r')
            data = f.read()
            f.close()
            return self.write(data)
    return self.write("<html><title>%(code)d: %(message)s</title>" \
            "<body class='bodyErrorPage'>%(code)d: %(message)s</body></html>" % {
        "code": status_code,
        "message": httplib.responses[status_code],
    })
