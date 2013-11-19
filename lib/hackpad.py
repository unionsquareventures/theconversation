from tornado import escape
from tornado.auth import _oauth10a_signature
import urllib
from urlparse import urljoin
import requests
import settings
import time
import binascii
import uuid
import logging
import sys

"""
Hackpad API. Documentation: https://hackpad.com/Public-Hackpad-API-Draft-nGhsrCJFlP7
"""

# Returns all of the pad IDs
def list_all():
  return do_api_request('pads/all', 'GET')

# Creates and returns the new pad ID
def create_hackpad():
  return do_api_request('pad/create', 'POST', {}, 'Hackpad Title\nHackpad contents.')

def do_api_request(path, method, post_data={}, body=''):
  try:
    url = urljoin('https://%s.hackpad.com/api/1.0/' % settings.get('hackpad_domain'), path)
    args = dict(
      oauth_consumer_key=escape.to_basestring(settings.get('hackpad_oauth_client_id')),
      oauth_signature_method='HMAC-SHA1',
      oauth_timestamp=str(int(time.time())),
      oauth_nonce=escape.to_basestring(binascii.b2a_hex(uuid.uuid4().bytes)),
      oauth_version='1.0a',
    )
    signature = _oauth10a_signature(
      {
        'key':settings.get('hackpad_oauth_client_id'),
        'secret':settings.get('hackpad_oauth_secret')
      },
      method,
      url,
      args
    )
    args['oauth_signature'] = signature
    api_link = url + '?' + urllib.urlencode(args)
    logging.info(api_link)

    hackpad = {}
    if method.lower() == 'post':
      r = requests.post(
        api_link,
        data=body,
        headers={'Content-Type': 'text/plain'},
        verify=False
      )
      hackpad = r.json
    else:
      r = requests.get(
        api_link,
        headers={'Content-Type': 'text/plain'},
        verify=False
      )
      hackpad = r.json
  except:
    logging.info(sys.exc_info()[0])
    hackpad = {}

  return hackpad
