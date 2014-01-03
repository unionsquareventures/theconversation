import base64
import hashlib
import hmac
import json
import re
import requests
import settings
import time

from lib import postsdb
from lib import userdb
from lib import template_helpers

import logging

def check_for_thread(short_code, link):
  api_link = 'https://disqus.com/api/3.0/threads/details.json?api_key=%s&thread:link=%s&forum=%s' % (settings.get('disqus_public_key'), link, short_code)
  return do_api_request(api_link, 'GET')

def create_thread(post, access_token):
  api_link = 'https://disqus.com/api/3.0/threads/create.json'
  url = "http://" + template_helpers.post_permalink(post)
  thread_info = {
    'forum': settings.get('disqus_short_code'),
    'title': post['title'].encode('utf-8'),
    'identifier':post['slug'],
    'url': url,
    'api_secret':settings.get('disqus_secret_key'),
    'api_key': settings.get('disqus_public_key'),
    'access_token': access_token
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

#
# Subscribe to a thread
#
def subscribe_to_thread(thread_id, access_token):
  api_link = 'https://disqus.com/api/3.0/threads/subscribe.json'
  info = {
    'api_secret': settings.get('disqus_secret_key'),
    'api_key': settings.get('disqus_public_key'),
    'access_token': access_token,
    'thread': thread_id,
  }
  return do_api_request(api_link, 'POST', info)

#
# Subscribe to all your threads
#
def subscribe_to_all_your_threads(username):
  account = userdb.get_user_by_screen_name(username)
  # todo: get disqus_user_id
  # temp: nick's ID
  if 'disqus_user_id' not in account:
    return
  
  threads = get_all_threads(account['disqus_user_id'])['response']
  my_threads = []
  for thread in threads:
    if 'link' not in thread or thread['link'] is None:
      continue
    if thread['link'].find('http://localhost') >= 0:
      continue
    my_threads.append(thread)
  if 'disqus_access_token' in account:
    for thread in my_threads:
      subscribe_to_thread(thread['id'], account['disqus_access_token'])
  return
  

def remove_all_your_threads(username):
  #account = userdb.get_user_by_screen_name(username)
  #get posts from disqus
  threads = get_all_threads(851030)
  for i, thread in enumerate(threads['response']):
    if thread['link'].find('http://localhost') == 0:
      print thread['link']
      print "----%s" % thread['identifiers']
      print "----%s" % thread['author']
      print "----%s" % thread['id']
      #print remove_thread(thread['id'])

def user_details(api_key, access_token, api_secret, user_id):
  api_link = 'https://disqus.com/api/3.0/users/details.json?access_token=%s&api_key=%s&api_secret=%s&user=%s' % (access_token, api_key, api_secret, int(user_id))
  return do_api_request(api_link)

#
# Get Threads
#
def get_all_threads(disqus_user_id=None):
  api_link = 'https://disqus.com/api/3.0/threads/list.json'
  info = {
    'api_secret': settings.get('disqus_secret_key'),
    'forum': settings.get('disqus_short_code'),
    'limit': 100
  }
  if disqus_user_id:
    info.update({
      'author': disqus_user_id
    })
  return do_api_request(api_link, 'GET', info)

def remove_thread(thread_id=None):
  if not thread_id:
    return
  api_link = 'https://disqus.com/api/3.0/threads/remove.json'
  info = {
    'api_secret': settings.get('disqus_secret_key'),
    'forum': settings.get('disqus_short_code'),
    'thread': thread_id,
    'access_token': "0a75d127c53f4a99bd853d721166af14"
  }
  return do_api_request(api_link, 'POST', info)


#####################################################
#### ACTUALLY HANDLE THE REQUESTS/RESPOSNE TO THE API
#####################################################
def do_api_request(api_link, method='GET', params={}):
  try:
    if method.upper() == 'GET':
      if len(params.keys()) > 0:
        r = requests.get(
          api_link,
          params=params,
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
        params=params,
        verify=False
      )
    disqus = r.json()
  except:
    disqus = {}
  return disqus
