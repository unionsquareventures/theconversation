import settings
from datetime import datetime
from postsdb import Post
from mongoengine import *


class Mentions(Document):
    def __init__(self, *args, **kwargs):
        super(Mentions, self).__init__(*args, **kwargs)
        db = self._get_db()

    screen_name = StringField()
    slug = StringField()
    date_created = DateTimeField()

def add_mention(screen_name, slug):
    """
    Adds a Mention object to the database
    # return db.mentions.update({'screen_name': screen_name, 'slug': slug}, {'screen_name': screen_name, 'slug': slug, 'date_created': datetime.utcnow()}, upsert=True)
    """
    mention, flag  = Mentions.objects.get_or_create(screen_name=screen_name, slug=slug, date_created=datetime.utcnow())
    return mention

def get_mentions_by_user(screen_name, per_page, page):
    mentions = Mentions.objects(screen_name=screen_name).order_by('-date_created').skip((page-1)*per_page).limit(per_page)
    posts = []
    for mention in mentions:
        posts.append(Post.objects.get(slug=mention.slug))
    return posts
