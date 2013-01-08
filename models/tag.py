from mongoengine import *

class Tag(Document):
    meta = {
        'indexes': ['name'],
    }
    name = StringField(required=True)
