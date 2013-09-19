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
            if not response:
                return
            thread_id = response['id']
            disqus.subscribe(lambda x: None, user_info, thread_id)

        # Subscribe the user to thread if it was created successfully.
        # Otherwise retrieve the thread ID and the subscribe them.
        def _created(response):
            if not response:
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
        next = self.get_argument('next', '')
        subscribe_to = self.get_argument('subscribe_to', '')
        u = UserInfo.objects.get(user__id_str=self.get_current_user_id_str())
        self.vars.update({
            'email': u.email_address or '',
            'error': '',
            'next': next,
            'subscribe_to': subscribe_to,
            'status': 'enter_email',
        })
        self.render('email/index.html', **self.vars)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        self.next = self.get_argument('next', '')
        self.email = self.get_argument('email', '')
        self.subscribe_to = self.get_argument('subscribe_to', '')
        self.token = str(uuid.uuid4())
        self.link = 'http://%s/auth/email/?token=%s' % (settings.base_url, self.token)
        id_str = self.get_current_user_id_str()
        u = UserInfo.objects.get(user__id_str=id_str)
        # Clear the existing email address
        if not self.email:
            u.email_address = ''
            self.set_secure_cookie('email_address', '')
            u.save()
            self.vars.update({
                'email': '',
                'error': '',
                'next': self.next,
                'subscribe_to': self.subscribe_to,
                'status': 'enter_email_cleared',
            })
            self.render('email/index.html', **self.vars)
            return
        existing = UserInfo.objects(email_address=self.email).first()
        if existing and existing.user.id_str != id_str:
            self.vars.update({
                'email': self.email or '',
                'error': 'This email address is already in use.',
                'next': self.next,
                'subscribe_to': self.subscribe_to,
                'status': 'enter_email',
            })
            self.render('email/index.html', **self.vars)
            return
        u.email_address = self.email
        u.save()
        self.set_secure_cookie('email_address', self.email)
        if self.subscribe_to:
            p = Post.objects.get(id=self.subscribe_to)
            self.subscribe(u, p)
        self.redirect(self.next or '/')
