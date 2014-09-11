import pymongo
import settings
from mongo import db
from mongoengine import *

# For update_twitter
import tweepy
import urllib2
from datetime import datetime

class User(EmbeddedDocument):
    id_str = StringField(required=True)
    auth_type = StringField(required=True)
    username = StringField(required=True)
    fullname = StringField(required=True)
    screen_name = StringField(required=True)
    profile_image_url_https = StringField(required=True)
    profile_image_url = StringField(required=True)
    is_blacklisted = BooleanField(default=False)

class AccessToken(EmbeddedDocument):
    secret = StringField(required=True)
    user_id = IntField(required=True)
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
    last_login = DateTimeField(default=datetime.now())
    date_created = DateTimeField(default=datetime.now())
    wants_daily_email = BooleanField(default=True)
    wants_email_alerts = BooleanField(default=True)
    disqus = DictField()
    tags = ListField()
    
#db.user_info.ensure_index('user.screen_name')

def get_all():
    return UserInfo.objects()

def get_user_by_id_str(id_str):
    return UserInfo.objects(user__id_str=id_str).first()

def get_user_by_screen_name(screen_name):
    return UserInfo.objects(user__screen_name=screen_name).first()

def get_user_by_email(email_address):
    return UserInfo.objects(email_address=email_address).first()

def get_disqus_users():
    return UserInfo.objects(disqus__exists=true)

def get_newsletter_recipients():
    return UserInfo.objects(wants_daily_email=True)

def create_new_user(user, access_token):
    user_info_dict = {
        'user': user,
        'access_token': access_token
    }
    user_info = UserInfo(**user_info_dict)
    return user_info.save()

def get_user_count():
    return len(UserInfo.objects())

def add_tags_to_user(screen_name, tags=[]):
    # return db.user_info.update({'user.screen_name':screen_name}, {'$addToSet':{'tags':{'$each':tags}}})
    u = UserInfo.objects.get(user__screenname=screen_name)
    for t in tags:
        if t not in u.tags:
            u.tags.append(t)
    return u

###########################
### SCRIPT FUNCTIONS
###########################
''' Updates twitter account of id id_str, or else updates all twitter accounts.
    Updating all accounts will probably cause API to puke from too many requests '''
def update_twitter(id_str=None, api=None):
    if not api:
        consumer_key = settings.get('twitter_consumer_key')
        consumer_secret = settings.get('twitter_consumer_secret')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
        api = tweepy.API(auth)

    if id_str:
        users = [get_user_by_id_str(id_str)]
    else:
        users = get_all()

    for u in users:
        id_str = u.user.id_str
        twitter_user = api.get_user(id=id_str)
        if id_str != twitter_user.id_str:
            raise Exception

        # Update UserInfo.user with new data from Twitter
        u.user.auth_type = 'twitter'
        u.user.id_str = twitter_user.id_str
        u.user.username = twitter_user.screen_name
        u.user.fullname = twitter_user.name
        u.user.screen_name = twitter_user.screen_name
        u.user.profile_image_url = twitter_user.profile_image_url
        u.user.profile_image_url_https = twitter_user.profile_image_url_https
        u.save()

        print "++ Updated user @%s" % u.user.username
        user_posts = postsdb.get_posts_by_screen_name(twitter_user.screen_name, per_page=100, page=1)
        for p in user_posts:
            p.user = u.user
            p.save()
            print "++++ Updated %s info for %s" % (p.user.screen_name, p.title)

''' Only updates a user if their twitter profile image URL returns a 404 '''
def update_twitter_profile_images():
    consumer_key = settings.get('twitter_consumer_key')
    consumer_secret = settings.get('twitter_consumer_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
    api = tweepy.API(auth)

    for user in get_all():
        print "Checking user %s" % user.user.screen_name
        try:
            response= urllib2.urlopen(user.user.profile_image_url_https)
        except urllib2.HTTPError, e:
            if e.code == 404:
                update_twitter(id_str=user.user.id_str, api=api)
