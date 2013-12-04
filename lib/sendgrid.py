# Copyright 2011 The greplin-tornado-sendgrid Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# modified 2013 - USV

"""Mixin for Sendgrid's REST API"""

import urllib
import functools
from tornado import httpclient, escape
import logging

class Sendgrid(object):
  """Base Sendgrid object"""

  _BASE_URL = "https://sendgrid.com/api/mail.send"
  _FORMAT = "json"

  _attrs = frozenset(['toname', 'x-smtpapi', 'fromname', 'replyto', 'date', 'files'])
  _required_attrs = frozenset(['to', 'subject', 'from'])


  def __init__(self, user, secret, sentry_client):
    self._user = user
    self._secret = secret
    self._sentry_client = sentry_client


  def send_email(self, callback, **kwargs):
    if 'text' not in kwargs and 'html' not in kwargs:
      msg = "Sendgrid message not sent. 'text' or 'html' fields required: %s" % str(kwargs)
      logging.warning(msg)
      self._sentry_client.captureMessage('[Sendgrid API] "send_email" error', msg=msg)
      callback(None)
      return
    for required in self._required_attrs:
      if required not in kwargs:
        logging.error("Message not sent. Missing required argument %s. %s" % (required, str(kwargs)))
        callback(None)
        return
    kwargs.update({'api_user':self._user, 'api_key':self._secret})
    api_url = "%s.%s" % (self._BASE_URL, self._FORMAT)
    post_body = urllib.urlencode(kwargs)
    http = httpclient.AsyncHTTPClient()
    request = httpclient.HTTPRequest(api_url, method='POST', body=post_body)
    try:
        http.fetch(request, functools.partial(self._on_sendgrid_result, callback, kwargs))
    except httpclient.HTTPError:
        pass


  def _on_sendgrid_result(self, callback, kwargs, result):
    result = escape.json_decode(result.body)
    if result.get("errors"):
      logging.warning('[Sendgrid API] "mail.send" error %s: %s' % (result, str(kwargs)))
      self._sentry_client.captureMessage('[Sendgrid API] "mail.send" error', result=result, kwargs=kwargs)
      callback(None)
      return
    callback(True)

