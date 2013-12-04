from mongoengine import *

class EmailVerification(Document):
    meta = {
            'indexes': ['token', 'user_id_str'],
    }
    email_address = StringField(required=True)
    user_id_str = StringField(required=True)
    token = StringField(required=True)
    next = StringField(required=False)
    subscribe_to = StringField(required=False)

