import settings
from mongoengine import *
from urlparse import urlparse
mongodb_db = urlparse(settings.mongodb_url).path[1:]
connect(mongodb_db, host=settings.mongodb_url)

class Tag(Document):
    meta = {
        'indexes': ['name'],
    }
    name = StringField(required=True)
