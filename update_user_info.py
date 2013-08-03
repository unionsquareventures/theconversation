"""
update_user_info
    Synchronizes the cached Twitter user information with the Twitter API.

Some portions are repurposed from https://github.com/facebook/tornado/blob/master/tornado/auth.py
"""

from tornado.auth import TwitterMixin
from tornado import escape
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
from tornado import httpclient
from tornado.util import bytes_type, u, unicode_type, ArgReplacer
import settings
from models.user_info import UserInfo, User
from models.post import Post
import time
import binascii
import uuid
import urlparse
import urllib as urllib_parse
import hmac
import hashlib
from raven.contrib.tornado import AsyncSentryClient

def run():
    print "Starting..."
    io = IOLoop.instance()
    uui = UpdateUserInfo(io)
    io.add_callback(uui.start_update)
    io.start()


class AuthError(Exception):
    pass


class UpdateUserInfo(object):
    _OAUTH_REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize"
    _OAUTH_AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate"
    _OAUTH_NO_CALLBACKS = False
    _TWITTER_BASE_URL = "https://api.twitter.com/1.1"


    def __init__(self, io):
        self.twitter_consumer_key = settings.tornado_config['twitter_consumer_key']
        self.twitter_consumer_secret = settings.tornado_config['twitter_consumer_secret']
        self.outbound_requests = 0
        self.io = io
        self.sentry = AsyncSentryClient(settings.sentry_dsn)

    def start_update(self):
        user_info = UserInfo.objects.all().fields(access_token=True)
        for info in user_info:
            self.outbound_requests += 1
            self.twitter_request('/users/sshow',
                    access_token=info.access_token._data,
                    user_id=info.access_token.user_id)

    def update_user(self, user_obj):
        user = {
                'auth_type': 'twitter',
                'id_str': user_obj['id_str'],
                'username': user_obj['screen_name'],
                'fullname': user_obj['name'],
                'screen_name': user_obj['screen_name'],
                'profile_image_url': user_obj['profile_image_url'],
                'profile_image_url_https': user_obj['profile_image_url_https'],
        }
        u = User(**user)
        UserInfo.objects(user__id_str=u.id_str).update(set__user=u)
        Post.objects(user__id_str=u.id_str).update(set__user=u)
        self.outbound_requests -= 1
        if self.outbound_requests == 0:
            self.io.stop()

    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()

    def _oauth_consumer_token(self):
        return dict(
            key=self.twitter_consumer_key,
            secret=self.twitter_consumer_secret)


    def _oauth_request_parameters(self, url, access_token, parameters={},
                                  method="GET"):
        """Returns the OAuth parameters as a dict for the given request.

        parameters should include all POST arguments and query string arguments
        that will be sent with the request.
        """
        consumer_token = self._oauth_consumer_token()
        base_args = dict(
            oauth_consumer_key=escape.to_basestring(consumer_token["key"]),
            oauth_token=escape.to_basestring(access_token["key"]),
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp=str(int(time.time())),
            oauth_nonce=escape.to_basestring(binascii.b2a_hex(uuid.uuid4().bytes)),
            oauth_version="1.0",
        )
        args = {}
        args.update(base_args)
        args.update(parameters)
        if getattr(self, "_OAUTH_VERSION", "1.0a") == "1.0a":
            signature = _oauth10a_signature(consumer_token, method, url, args,
                                            access_token)
        else:
            signature = _oauth_signature(consumer_token, method, url, args,
                                         access_token)
        base_args["oauth_signature"] = escape.to_basestring(signature)
        return base_args


    def twitter_request(self, path, access_token=None,
                        post_args=None, **args):
        if path.startswith('http:') or path.startswith('https:'):
            # Raw urls are useful for e.g. search which doesn't follow the
            # usual pattern: http://search.twitter.com/search.json
            url = path
        else:
            url = self._TWITTER_BASE_URL + path + ".json"
        # Add the OAuth resource request signature if we have credentials
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args:
            url += "?" + urllib_parse.urlencode(args)
        http = self.get_auth_http_client()
        http_callback = self._on_twitter_request
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=http_callback)
        else:
            http.fetch(url, callback=http_callback)

    def _on_twitter_request(self, response):
        if response.error:
            self.sentry.captureMessage("[Twitter] Error response %s fetching %s" % (response.error, response.request.url))
            self.outbound_requests -= 1
            if self.outbound_requests == 0:
                self.io.stop()
            return
        self.update_user(escape.json_decode(response.body))


def _oauth_escape(val):
    if isinstance(val, unicode_type):
        val = val.encode("utf-8")
    return urllib_parse.quote(val, safe="~")


def _oauth_parse_response(body):
    # I can't find an officially-defined encoding for oauth responses and
    # have never seen anyone use non-ascii.  Leave the response in a byte
    # string for python 2, and use utf8 on python 3.
    body = escape.native_str(body)
    p = urlparse.parse_qs(body, keep_blank_values=False)
    token = dict(key=p["oauth_token"][0], secret=p["oauth_token_secret"][0])

    # Add the extra parameters the Provider included to the token
    special = ("oauth_token", "oauth_token_secret")
    token.update((k, p[k][0]) for k in p if k not in special)
    return token


def _oauth10a_signature(consumer_token, method, url, parameters={}, token=None):
    """Calculates the HMAC-SHA1 OAuth 1.0a signature for the given request.

    See http://oauth.net/core/1.0a/#signing_process
    """
    parts = urlparse.urlparse(url)
    scheme, netloc, path = parts[:3]
    normalized_url = scheme.lower() + "://" + netloc.lower() + path

    base_elems = []
    base_elems.append(method.upper())
    base_elems.append(normalized_url)
    base_elems.append("&".join("%s=%s" % (k, _oauth_escape(str(v)))
                               for k, v in sorted(parameters.items())))

    base_string = "&".join(_oauth_escape(e) for e in base_elems)
    key_elems = [escape.utf8(urllib_parse.quote(consumer_token["secret"], safe='~'))]
    key_elems.append(escape.utf8(urllib_parse.quote(token["secret"], safe='~') if token else ""))
    key = b"&".join(key_elems)

    hash = hmac.new(key, escape.utf8(base_string), hashlib.sha1)
    return binascii.b2a_base64(hash.digest())[:-1]


def _oauth_signature(consumer_token, method, url, parameters={}, token=None):
    """Calculates the HMAC-SHA1 OAuth signature for the given request.

    See http://oauth.net/core/1.0/#signing_process
    """
    parts = urlparse.urlparse(url)
    scheme, netloc, path = parts[:3]
    normalized_url = scheme.lower() + "://" + netloc.lower() + path

    base_elems = []
    base_elems.append(method.upper())
    base_elems.append(normalized_url)
    base_elems.append("&".join("%s=%s" % (k, _oauth_escape(str(v)))
                               for k, v in sorted(parameters.items())))
    base_string = "&".join(_oauth_escape(e) for e in base_elems)

    key_elems = [escape.utf8(consumer_token["secret"])]
    key_elems.append(escape.utf8(token["secret"] if token else ""))
    key = b"&".join(key_elems)

    hash = hmac.new(key, escape.utf8(base_string), hashlib.sha1)
    return binascii.b2a_base64(hash.digest())[:-1]


if __name__ == '__main__':
    run()
