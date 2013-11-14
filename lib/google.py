# -*- coding: utf-8 -*-

"""
Basic google link shortener api handler - https://developers.google.com/url-shortener/v1/getting_started
"""

import requests
import simplejson as json
import settings

def shorten_url(url):
  goo_key = settings.get('google_api_key')
  r = requests.post(
    'https://www.googleapis.com/urlshortener/v1/url?key=%s' % goo_key,
    data=json.dumps({'longUrl': url}),
    headers={'Content-Type': 'application/json; charset=UTF-8'},
    verify=False
  )
  return json.loads(r.text)

def expand_url(url):
  r = requests.get(
    'https://www.googleapis.com/urlshortener/v1/url?shortUrl=%s' % url,
    verify=False
  )
  return json.loads(r.text)

