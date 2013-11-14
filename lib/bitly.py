import bitly_api
import settings

def shorten_url(url):
  access_token = settings.get('bitly_access_token')
  c = bitly_api.Connection(access_token=access_token)
  return c.shorten(url)

def expand_url(hash_val):
  access_token = settings.get('bitly_access_token')
  c = bitly_api.Connection(access_token=access_token)
  return c.expand(hash_val)
