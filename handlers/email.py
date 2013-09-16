import tornado
from base import BaseHandler
from models.user_info import UserInfo
from models.email_verification import EmailVerification
from models.post import Post
import uuid
import settings

class EmailHandler(BaseHandler):
    def subscribe(self, u, post):
        # Attempt to create the post's thread
        user_url = 'http://www.twitter.com/%s' % u.user.screen_name
        user_info = {
                'id': u.user.id_str,
                'username': u.user.username,
                'email': u.email_address,
                'avatar': u.user.profile_image_url,
                'url': user_url,
        }
        # Subscribe the OP to the thread
        disqus = self.settings['disqus']

        # Subscribe a user to the thread specified in response
        def _subscribe(response):
            print "== SUBSCRIBE"
            if not response:
                return
            thread_id = response['id']
            disqus.subscribe(lambda x: None, user_info, thread_id)

        # Subscribe the user to thread if it was created successfully.
        # Otherwise retrieve the thread ID and the subscribe them.
        def _created(response):
            print "== CREATED"
            if not response:
                print "== DETAILS"
                disqus.thread_details(_subscribe, post.id)
            else:
                _subscribe(response)

        # Attempt to create the thread.
        thread_info = {
                'title': post.title.encode('utf-8'),
                'identifier': post.id,
        }
        disqus.create_thread(_created, user_info, thread_info)

    @tornado.web.authenticated
    def get(self):
        token = self.get_argument('token', '')
        if token:
            ev = EmailVerification.objects.get(token=token)
            id_str = self.get_current_user_id_str()
            if id_str != ev.user_id_str:
                raise tornado.web.HTTPError(500)
            u = UserInfo.objects.get(user__id_str=id_str)
            u.email_address = ev.email_address
            u.save()
            ev.delete()
            self.set_secure_cookie('email_address', ev.email_address)
            if ev.subscribe_to:
                p = Post.objects.get(id=ev.subscribe_to)
                self.subscribe(u, p)
            self.vars.update({
                'email': ev.email_address,
                'next': ev.next or '/',
                'errors': '',
                'status': 'email_verified',
            })
            self.render('email/index.html', **self.vars)
            return
        next = self.get_argument('next', '')
        subscribe_to = self.get_argument('subscribe_to', '')
        u = UserInfo.objects.get(user__id_str=self.get_current_user_id_str())
        self.vars.update({
            'email': u.email_address or '',
            'errors': '',
            'next': next,
            'subscribe_to': subscribe_to,
            'status': 'enter_email',
        })
        self.render('email/index.html', **self.vars)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        self.next = self.get_argument('next', '')
        self.email = self.get_argument('email')
        self.subscribe_to = self.get_argument('subscribe_to', '')
        self.token = str(uuid.uuid4())
        self.link = 'http://%s/auth/email/?token=%s' % (settings.base_url, self.token)

        sendgrid = self.settings['sendgrid']
        sendgrid.send_email(self._on_sendgrid, **{
            'from': 'no_reply@usv.com',
            'to': self.email,
            'subject': "USV.com - Please verify your email address",
            'text': "Please verify your email address by navigating to this link: %s" % self.link,
        })

    @tornado.web.asynchronous
    def _on_sendgrid(self, success):
        if not success:
            raise tornado.web.HTTPError(500)

        v = EmailVerification(**{
            'email_address': self.email,
            'user_id_str': self.get_secure_cookie('user_id_str'),
            'next': self.next,
            'subscribe_to': self.subscribe_to,
            'token': self.token,
        })
        v.save()
        self.vars.update({
            'email': self.email,
            'errors': '',
            'next': self.next,
            'status': 'verification_email',
        })
        self.render('email/index.html', **self.vars)
