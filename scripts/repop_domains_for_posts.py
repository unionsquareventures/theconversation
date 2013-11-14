# repopulate the domain value for each post

import requests
import simplejson as json
import urlparse
from mongo import db

def expand_url(url):
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
    long_url = expand_url(post['url'])
  domain = urlparse(long_url).netloc
  post['domain'] = domain
  db.post.update({'_id':post['_id']}, {'$set':{'domain':domain}})
  print "updated %s" % post['slug']

