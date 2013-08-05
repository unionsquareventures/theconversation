import sys
sys.path.append('../')
import settings
import nose
import unittest
import time
from models.post import Post
from models.user_info import User, VotedUser
import redis
import datetime as dt
from mock_data import mock_data
import time
import mongoengine

class TestPost(unittest.TestCase):
    def setUp(self):
        db = Post._get_db()
        for name in db.collection_names():
            if name not in ['system.indexes']:
                db.drop_collection(name)
        Post.ensure_indexes()
        self.redis = redis.StrictRedis.from_url(settings.redis_url)
        self.redis.flushdb()
        self.test_user_attrs = {
                'auth_type': 'twitter',
                'fullname': 'USV',
                'username': u'usv',
                'screen_name': u'usv',
                'profile_image_url_https': u'https://si0.twimg.com/profile_images/54821022/USVLogo_normal.gif',
                'profile_image_url': u'http://a0.twimg.com/profile_images/54821022/USVLogo_normal.gif',
                'id_str': u'14946614'
        }
        self.maxDiff = 100000
        self.test_post1_attrs = dict(
                title="Qualified Small Business Stock",
                user=User(**self.test_user_attrs),
                date_created=dt.datetime.now(),
                votes=1,
                voted_users=[VotedUser(id=self.test_user_attrs['id_str'])],
                body_raw=mock_data('post', '1', 'raw'),
                body_html=mock_data('post', '1', 'html'),
                body_text=mock_data('post', '1', 'text'),
                body_truncated=mock_data('post', '1', 'truncated'),
        )

    # Test creating a post, ensure slug exists, etc.
    def test_create_post(self):
        p = Post(**self.test_post1_attrs)
        p.save()

        p = Post.objects(id=p.id).first()
        def check(k, norm=lambda x: x):
            self.assertEqual(norm(getattr(p, k)), norm(self.test_post1_attrs[k]))
        check('body_raw')
        check('body_html')
        check('body_text')
        check('body_truncated')
        check('votes')
        check('date_created', norm=lambda x: time.mktime(x.timetuple()))
        check('title')
        check('user')
        check('voted_users')
        self.assertEqual(p.slug, 'qualified-small-business-stock')
        self.assertFalse(p.featured)
        self.assertFalse(p.date_featured)
        self.assertFalse(p.deleted)
        self.assertFalse(p.date_deleted)
        self.assertFalse(p.url)
        self.assertFalse(p.hackpad_url)
        self.assertFalse(p.has_hackpad)

    # Post without a body
    def test_create_no_body(self):
        attrs = dict(self.test_post1_attrs)
        del attrs['body_raw']
        del attrs['body_html']
        del attrs['body_text']
        del attrs['body_truncated']
        p = Post(**attrs)
        with self.assertRaises(mongoengine.ValidationError) as cm:
            p.save()

    # Test query for a post by slug
    def test_slug_query(self):
        attrs = dict(self.test_post1_attrs)
        p = Post(**attrs)
        p.save()
        p = Post.objects(slug='qualified-small-business-stock').first()
        self.assertIsNotNone(p)

    # Test changing the post title
    # Test creating a post with a pre-existing URL
    # Test creating a post with a pre-existing slug
    # Test body length limit
    # Test invalid hackpad URL

    def tearDown(self):
        db = Post._get_db()
        for name in db.collection_names():
            if name not in ['system.indexes']:
                db.drop_collection(name)
        self.redis = redis.StrictRedis.from_url(settings.redis_url)
        self.redis.flushdb()
