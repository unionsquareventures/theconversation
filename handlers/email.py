import tornado
from base import BaseHandler
from models.user_info import UserInfo
from models.email_verification import EmailVerification
import uuid
import settings

class EmailHandler(BaseHandler):
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
            self.vars.update({
                'email': ev.email_address,
                'next': ev.next,
                'errors': '',
                'status': 'email_verified',
            })
            self.render('email/index.html', **self.vars)
            return
        next = self.get_argument('next', '')
        u = UserInfo.objects.get(user__id_str=self.get_current_user_id_str())
        self.vars.update({
            'email': u.email_address or '',
            'errors': '',
            'next': next,
            'status': 'enter_email',
        })
        self.render('email/index.html', **self.vars)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        self.next = self.get_argument('next', '')
        self.email = self.get_argument('email')
        self.token = str(uuid.uuid4())
        self.link = 'http://%s/auth/email/?token=%s' % (settings.base_url, self.token)

        sendgrid = self.settings['sendgrid']
        sendgrid.send_email(self._on_sendgrid, **{
            'from': 'no_reply@usv.com',
            'to': self.email,
            'subject': "USV.com - Please verify your email address",
            'text': "Navigate to this link to verify your address: %s" % self.link,
        })

    @tornado.web.asynchronous
    def _on_sendgrid(self, success):
        if not success:
            raise tornado.web.HTTPError(500)

        v = EmailVerification(**{
            'email_address': self.email,
            'user_id_str': self.get_secure_cookie('user_id_str'),
            'next': self.next,
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
        self.finish()
