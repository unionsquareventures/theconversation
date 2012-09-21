from mongoengine import *

class User(EmbeddedDocument):
    auth_type = StringField(required=True)
    username = StringField(required=True)
    screen_name = StringField(required=True)
    profile_image_url_https = StringField(required=True)
    profile_image_url = StringField(required=True)

