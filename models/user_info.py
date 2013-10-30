from mongoengine import *

class User(EmbeddedDocument):
    id_str = StringField(required=True)
    auth_type = StringField(required=True)
    username = StringField(required=True)
    fullname = StringField(required=True)
    screen_name = StringField(required=True)
    profile_image_url_https = StringField(required=True)
    profile_image_url = StringField(required=True)
    is_blacklisted = BooleanField(default=False)

class VotedUser(EmbeddedDocument):
    id = StringField(required=True, primary_key=True)
    username = StringField()

class AccessToken(EmbeddedDocument):
    secret = StringField(required=True)
    user_id = StringField(required=True)
    screen_name = StringField(required=True)
    key = StringField(required=True)

class UserInfo(Document):
    meta = {
        'indexes': ['user.id_str', 'email_address', 'user.username']
    }
    user = EmbeddedDocumentField(User, required=True)
    access_token = EmbeddedDocumentField(AccessToken, required=True)
    email_address = StringField(required=False)
    role = StringField(default="user")
    
    def editlink(self):
        link = '%s/collections/user_info/documents/%s' % (os.environ.get('MONGODB_CLOUD_BASE_URL'), self.id)
        return link
