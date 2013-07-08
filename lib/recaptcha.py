# Copyright (c) 2012, Hsiaoming Yang
# https://github.com/lepture/tornado.third/blob/master/recaptcha.py
# Modified 2013, Zach Cimafonte

import settings
import logging
import urllib
from tornado import httpclient


class RecaptchaMixin(object):
    """RecaptchaMixin

    You must define some settings for this mixin. All information
    can be found at http://www.google.com/recaptcha

    A basic example::

        Define recaptcha_key, recaptcha_secret, and recaptcha_theme
        in the project settings.

        class SignupHandler(RequestHandler, RecaptchaMixin):
            def get(self):
                self.write('<form method="post" action="">')
                self.write(self.xsrf_form_html())
                self.write(self.recaptcha_render())
                self.write('<button type="submit">Submit</button>')
                self.write('</form>')

            @asynchronous
            def post(self):
                self.recaptcha_validate(self._on_validate)

            def _on_validate(self, response):
                if response:
                    self.write('success')
                    self.finish()
                    return
                self.write('failed')
                self.finish()
    """

    RECAPTCHA_VERIFY_URL = "http://www.google.com/recaptcha/api/verify"

    def recaptcha_render(self):
        token = self._recaptcha_token()
        html = (
            '<div id="recaptcha_div"></div>'
            '<script type="text/javascript" '
            'src="https://www.google.com/recaptcha/api/js/recaptcha_ajax.js">'
            '</script><script type="text/javascript">'
            'Recaptcha.create("%(key)s", "recaptcha_div", '
            '{theme: "%(theme)s",callback:Recaptcha.focus_response_field});'
            '</script>'
        )
        return html % token

    def recaptcha_validate(self, callback):
        token = self._recaptcha_token()
        challenge = self.get_argument('recaptcha_challenge_field', None)
        response = self.get_argument('recaptcha_response_field', None)
        callback = self.async_callback(self._on_recaptcha_request, callback)
        http = httpclient.AsyncHTTPClient()
        post_args = {
            'privatekey': token['secret'],
            'remoteip': self.request.remote_ip,
            'challenge': challenge,
            'response': response
        }
        http.fetch(self.RECAPTCHA_VERIFY_URL, method="POST",
                   body=urllib.urlencode(post_args), callback=callback)

    def _on_recaptcha_request(self, callback, response):
        if response.error:
            logging.warning("Error response %s fetching %s", response.error,
                    response.request.url)
            callback(None)
            return
        verify, message = response.body.split()
        if verify == 'true':
            callback(response.body)
        else:
            logging.warning("Recaptcha verify failed %s", message)
            callback(None)

    def _recaptcha_token(self):
        token = dict(
            key=settings.recaptcha_key,
            secret=settings.recaptcha_secret,
            theme=settings.recaptcha_theme,
        )
        return token
