import sys
sys.path.append('../')
from server import init_app
import tornado
import socket
from tornado.testing import AsyncHTTPTestCase
from bs4 import BeautifulSoup
import settings
import Cookie
import os

class TestAuthHTTP(AsyncHTTPTestCase):
    def get_app(self):
        return init_app()

    # Required for Twitter OAuth
    def bind_port(self):
        [sock] = tornado.netutil.bind_sockets(8888, 'localhost', family=socket.AF_INET)
        port = sock.getsockname()[1]
        return sock, port

    def get_http_port(self):
        return self.__port

    def setUp(self):
        super(AsyncHTTPTestCase, self).setUp()
        sock, port = self.bind_port()
        self.__port = port

        self.http_client = self.get_http_client()
        self._app = self.get_app()
        self.http_server = self.get_http_server()
        self.http_server.add_sockets([sock])


    def _cookie_header(self, cookies):
        return ''.join(['%s=%s;' %(x, morsel.value)
                        for (x, morsel)
                        in cookies.items()])

    def test_auth_index_page(self):
        url = self.get_url('/auth/twitter/')
        self.http_client.fetch(url, self.stop, follow_redirects=False)
        response = self.wait()
        self.assertEqual(response.code, 302)

        c = response.headers['Set-Cookie']
        site_cookies = Cookie.SimpleCookie(c)
        self.http_client.fetch(response.headers['Location'], self.stop)
        response = self.wait()
        c = response.headers['Set-Cookie']
        c = c.replace('; HttpOnly,', ';')
        cookies = Cookie.SimpleCookie(c)
        soup = BeautifulSoup(response.body)
        form = soup.select('#oauth_form')[0]
        body = {
                'authenticity_token': soup.find_all(attrs={'name':'authenticity_token'})[0]['value'],
                'oauth_token': soup.find_all(attrs={'name': 'oauth_token'})[0]['value'],
                'session[username_or_email]': settings.test_twitter_username,
                'session[password]': settings.test_twitter_password,
                'remember_me': '0',
        }
        u = lambda x: tornado.escape.url_escape(unicode(x))
        body = '&'.join(['%s=%s' % (k, u(v)) for k, v in body.iteritems()])
        self.http_client.fetch(form['action'], self.stop, follow_redirects=False,
                                headers={'Cookie': self._cookie_header(cookies)},
                                method='POST', body=body)
        response = self.wait()
        self.assertEqual(response.code, 200)

        soup = BeautifulSoup(response.body)
        meta = soup.find_all('meta', attrs={'http-equiv': 'refresh'})[0]
        url = meta['content'].split(';url=')[1]
        c = response.headers['Set-Cookie']
        c = c.replace('; HttpOnly,', ';')
        c = c.replace('; secure,', ';')
        c = c.replace('GMT,', 'GMT;')
        cookies.load(c)
        self.http_client.fetch(url, self.stop, follow_redirects=False,
                                    headers={'Cookie': self._cookie_header(site_cookies)})
        response = self.wait()
        self.assertEqual(response.code, 302)

        c = response.headers['Set-Cookie']
        c = c.replace('; HttpOnly,', ';')
        c = c.replace('; secure,', ';')
        c = c.replace('GMT,', 'GMT;')
        site_cookies.load(c)
        self.http_client.fetch(self.get_url('/'), self.stop, follow_redirects=False,
                                    headers={'Cookie': self._cookie_header(site_cookies)})
        response = self.wait()
        soup = BeautifulSoup(response.body)
        self.assertEqual(response.code, 200)
