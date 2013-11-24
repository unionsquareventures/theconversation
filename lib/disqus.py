import base64
import hashlib
import hmac
import json
import re
import requests
import settings
import time

def check_for_thread(short_code, link):
  api_link = 'https://disqus.com/api/3.0/threads/details.json?api_key=%s&thread:link=%s&forum=%s' % (settings.get('disqus_public_key'), link, short_code)
  return do_api_request(api_link, 'GET')

def create_thread(title, identifier, user_info):
  api_link = 'https://disqus.com/api/3.0/threads/create.json'
  thread_info = {
    'forum': settings.get('disqus_short_code'),
    'title': title.encode('utf-8'),
    'identifier':identifier,
    'api_secret':settings.get('disqus_secret_key'),
    'remote_auth': get_sso(False, user_info)
  }
  return do_api_request(api_link, 'POST', thread_info)

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

def get_thread_details(thread_id):
  api_link = 'https://disqus.com/api/3.0/threads/details.json?api_key=%s&thread:ident=%s&forum=%s' % (settings.get('disqus_public_key'), thread_id, settings.get('disqus_short_code'))
  return do_api_request(api_link, 'GET')

def grep_short_code(link):
  # attempt to get the disqus short code out of a given page
  # http://continuations.disqus.com/embed.js vs. http://disqus.com/forums/avc/embed.js
  short_code = ''
  r = requests.get(link, verify=False)
  html = r.text
  m = re.search(r'http:\/\/disqus\.com\/forums\/([^/]+)', html)
  if m:
    short_code = m.group(1).strip()

  if short_code == '':
    m = re.search(r'http:\/\/([^.]+)\.disqus\.com', html)
    if m:
      short_code = m.group(1).strip()

  return short_code

def subscribe_to_thread(thread_id, user_info):
  api_link = 'https://disqus.com/api/3.0/threads/subscribe.json'
  info = {
    'api_secret': settings.get('disqus_secret_key'),
    'remote_auth': get_sso(False, user_info),
    'thread': thread_id,
  }
  return do_api_request(api_link, 'POST', info)

def user_details(api_key, access_token, api_secret, user_id):
  api_link = 'https://disqus.com/api/3.0/users/details.json?access_token=%s&api_key=%s&api_secret=%s&user=%s' % (access_token, api_key, api_secret, int(user_id))
  return do_api_request(api_link)

#####################################################
#### ACTUALLY HANDLE THE REQUESTS/RESPOSNE TO THE API
#####################################################
def do_api_request(api_link, method='GET', params={}):
  try:
    if method.upper() == 'GET':
      if len(params.keys()) > 0:
        r = requests.get(
          api_link,
          data=params,
          verify=False
        )
      else:
        r = requests.get(
          api_link,
          verify=False
        )
    else:
      r = requests.post(
        api_link,
        data=params,
        verify=False
      )
    disqus = r.json
  except:
    disqus = {}
  return disqus
