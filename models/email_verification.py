from mongoengine import *

class EmailVerification(Document):
    meta = {
            'indexes': ['token', 'user_id_str'],
    }
    email_address = StringField(required=True)
    user_id_str = StringField(required=True)
    next = StringField(required=True)
    token = StringField(required=True)

