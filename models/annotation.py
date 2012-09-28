from mongoengine import *

class AnnotationRange(EmbeddedDocument):
    start = StringField(required=True)
    end = StringField(required=True)
    startOffset = IntField(required=True)
    endOffset = IntField(required=True)

class Annotation(EmbeddedDocument):
    ranges = ListField(EmbeddedDocumentField(AnnotationRange), required=True)
    text = StringField(required=True)
    post_id = IntField(required=True)
    quote = StringField(required=True)

