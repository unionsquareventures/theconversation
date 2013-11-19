# repopulate the domain value for each post

import bitly_api
import requests
import simplejson as json
import urlparse
from mongo import db

def expand_bitly_url(hash_val):
  access_token = ''
  c = bitly_api.Connection(access_token=access_token)
  return c.expand(hash_val)['long_url']

def expand_google_url(url):
  r = requests.get(
    'https://www.googleapis.com/urlshortener/v1/url?shortUrl=%s' % url,
    verify=False
  )
  return json.loads(r.text)['longUrl']

# get all the existing posts
posts = list(db.post.find())
for post in posts:
  long_url = post['url']
  if long_url.find('goo.gl') > -1:
    long_url = expand_google_url(post['url'])
  if long_url.find('bit.ly') > -1 or long_url.find('bitly.com') > -1:
    long_url = expand_bitly_url(post['url'].replace('http://bitly.com','').replace('http://bit.ly',''))
  domain = urlparse(long_url).netloc
  post['domain'] = domain
  db.post.update({'_id':post['_id']}, {'$set':{'domain':domain}})
  print "updated %s" % post['slug']

