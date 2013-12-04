from tornado import escape
from tornado.auth import _oauth10a_signature
from tornado import httpclient
import urllib as urllib_parse
from urlparse import urljoin
import time
import binascii
import uuid
import json
from functools import partial

"""
A wrapper for the Hackpad API.

Documentation: https://hackpad.com/Public-Hackpad-API-Draft-nGhsrCJFlP7
"""
class HackpadAPI(object):
    def __init__(self, oauth_client_id, oauth_secret, domain='www'):
        self.consumer_token = dict(key=oauth_client_id, secret=oauth_secret)
        self.base_url = 'https://%s.hackpad.com/api/1.0/' % domain
        self.http = httpclient.AsyncHTTPClient()

    def _oauth_request(self, path, user_callback, **kwargs):
        url = urljoin(self.base_url, path)
        args = dict(
            oauth_consumer_key=escape.to_basestring(self.consumer_token['key']),
            oauth_signature_method='HMAC-SHA1',
            oauth_timestamp=str(int(time.time())),
            oauth_nonce=escape.to_basestring(binascii.b2a_hex(uuid.uuid4().bytes)),
            oauth_version='1.0a',
        )
        signature = _oauth10a_signature(self.consumer_token, kwargs.get('method', 'GET'), url, args)
        args['oauth_signature'] = signature
        req_url = url + '?' + urllib_parse.urlencode(args)
        # Fetch the response
        callback = partial(self._response, user_callback)
        self.http.fetch(req_url, callback, **kwargs)

    # Parse the JSON response, and invoke the provided callback
    def _response(self, user_callback, resp):
        resp_json = json.loads(resp.body)
        user_callback(resp_json)

    # Returns all of the pad IDs
    def list_all(self, user_callback):
        self._oauth_request('pads/all', user_callback)

    # Creates and returns the new pad ID
    def create(self, user_callback):
        self._oauth_request('pad/create', user_callback,
                                method='POST', headers={'Content-Type': 'text/plain'},
                                body="Hackpad Title\nHackpad contents.")

    # More methods can be added (see docs)
