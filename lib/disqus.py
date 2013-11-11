import base64
import cookielib
import hashlib
import hmac
import json
import mechanize
import settings
import time

def get_sso(format_html, user_info):
  # create a JSON packet of our data attributes
  data = json.dumps(user_info)
  # encode the data to base64
  message = base64.b64encode(data)
  # generate a timestamp for signing the message
  timestamp = int(time.time())
  # generate our hmac signature
  sig = hmac.HMAC(settings.get('disqus_secret_key'), '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
  if format_html:
    # return a script tag to insert the sso message
    return """this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";""" % dict(message=message, timestamp=timestamp, sig=sig, pub_key=settings.get('disqus_public_key'))
  else:
    return "%(message)s %(sig)s %(timestamp)s" % dict(message=message, timestamp=timestamp, sig=sig)

def get_post_details(post_id):
  message = {'id':'','message':'','author':{'username':'', 'email':''}}
  api_link = 'https://disqus.com/api/3.0/posts/details.json'
  api_key = settings.get('disqus_public_key')
  api_link = 'https://disqus.com/api/3.0/posts/details.json?api_key=%s&post=%s' % (api_key, post_id)
  disqus = do_api_request(api_link)
  if 'response' in disqus.keys():
    if 'id' in disqus['response'].keys():
      message['id'] = disqus['response']['id']
      message['message'] = disqus['response']['message']
      message['author']['username'] = disqus['response']['author']['username']
      if 'email' in disqus['response']['author'].keys():
        message['author']['email'] = disqus['response']['author']['email']
  return message

def do_api_request(api_link):
  try:
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    r = br.open(api_link)
    data = r.read()
    disqus = json.loads(data)
  except:
    disqus = {}
  return disqus
