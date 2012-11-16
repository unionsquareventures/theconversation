from mongoengine import *
c = connect('usv')

# Indexes

# Content
c['usv']['content'].ensure_index([('votes', -1)])
c['usv']['content'].ensure_index([('date_created', -1)])
c['usv']['content'].ensure_index([('tags', 1)])
c['usv']['content'].ensure_index([('id', 1)])

from post import Post
from link import Link
from tweet import Tweet
from question import Question
from annotation import Annotation, AnnotationRange
from tag import Tag
from content import Content

from user import User

