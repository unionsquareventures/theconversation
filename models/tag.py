from mongoengine import *

class Tag(Document):
    name = StringField(required=True)
