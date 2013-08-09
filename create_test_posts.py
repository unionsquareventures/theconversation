import models
import redis
import datetime as dt
from lib.score import calculate_score
import time

user = {
   'auth_type': 'twitter',
   'fullname': 'USV',
   'username': u'usv',
   'screen_name': u'usv',
   'profile_image_url_https': u'https://si0.twimg.com/profile_images/54821022/USVLogo_normal.gif',
   'profile_image_url': u'http://a0.twimg.com/profile_images/54821022/USVLogo_normal.gif',
   'id_str': u'14946614'
}

body = """Today, we have joined a large and diverse group of companies, non-profits and consumer advocates in an open letter urging the US government to allow internet and telecom companies to freely report statistics on government surveillance requests. As we've discussed before, standing up for your users is a feature. As we all move more and more of our lives online and into our phones, the data we are producing -- and sharing, whether we know it or not -- is growing exponentially. The extent to which we can trust the services we use to steward our data appropriately is a matter of global economic importance."""

r = redis.StrictRedis(host='localhost', port=6379, db=0)
for i in range(1, 101):
   d = dt.datetime.now()
   score = calculate_score(1, d)
   p = models.Post(title="Testing... %i" % i, body_raw = body, body_html=body, user=models.User(**user), score=score, date_created=d, votes=1, body_truncated=body, body_text=body)
   p.save()
   r.set('post:%s:votes' % p.id, 1)
   r.zadd('hot', score, p.id)
   r.zadd('new', time.mktime(d.timetuple()), p.id)