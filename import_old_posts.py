import csv
from bs4 import BeautifulSoup
from lib.sanitize import html_to_text
from models.post import Post
from models.user_info import User, VotedUser
import lib.sanitize as sanitize
from dateutil import parser
import time
from math import log
import json
import redis
import sys
import urllib2

users = {
	'3': {'auth_type': 'twitter', 'fullname': 'Fred Wilson', 'username': u'fredwilson', 'screen_name': u'fredwilson', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/3580641456/82c873940343750638b7caa04b4652fe_normal.jpeg', 'profile_image_url': u'https://si0.twimg.com/profile_images/3580641456/82c873940343750638b7caa04b4652fe_normal.jpeg', 'id_str': u'1000591'},
	'16': {'auth_type': 'twitter', 'fullname': 'Brian Watson', 'username': u'bwats', 'screen_name': u'bwats', 'profile_image_url_https': u'http://a0.twimg.com/profile_images/3241879304/52040f71651485eb490a89fba34360fc_normal.png', 'profile_image_url': u'https://si0.twimg.com/profile_images/3241879304/52040f71651485eb490a89fba34360fc_normal.png', 'id_str': u'1000591'},
	'15': {'auth_type': 'twitter', 'fullname': 'Andy Weissman', 'username': u'aweissman', 'screen_name': u'aweissman', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/1769514792/image1327099968_normal.png', 'profile_image_url': u'http://a0.twimg.com/profile_images/1769514792/image1327099968_normal.png', 'id_str': u'1374411'},
	'7': {'auth_type': 'twitter', 'fullname': 'Albert Wenger', 'username': u'albertwenger', 'screen_name': u'albertwenger', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/1773890030/aew_artistic_normal.gif', 'profile_image_url': u'http://a0.twimg.com/profile_images/1773890030/aew_artistic_normal.gif', 'id_str': u'7015112'},
	'11': {'auth_type': 'twitter', 'fullname': 'USV', 'username': u'usv', 'screen_name': u'usv', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/54821022/USVLogo_normal.gif', 'profile_image_url': u'http://a0.twimg.com/profile_images/54821022/USVLogo_normal.gif', 'id_str': u'14946614'},
	'1': {'auth_type': 'twitter', 'fullname': 'USV', 'username': u'usv', 'screen_name': u'usv', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/54821022/USVLogo_normal.gif', 'profile_image_url': u'http://a0.twimg.com/profile_images/54821022/USVLogo_normal.gif', 'id_str': u'14946614'},
	'18': {'auth_type': 'twitter', 'fullname': 'Alexander Pease', 'username': u'alexandermpease', 'screen_name': u'alexandermpease', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/2425968860/zg9wdsxlfgecxog9lkwz_normal.png', 'profile_image_url': u'http://a0.twimg.com/profile_images/2425968860/zg9wdsxlfgecxog9lkwz_normal.png', 'id_str': u'302134974'},
	'17': {'auth_type': 'twitter', 'fullname': 'Nick Grossman', 'username': u'nickgrossman', 'screen_name': u'nickgrossman', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/3608605926/71036b2e9d4deff52fdacd8196c40ce5_normal.png', 'profile_image_url': u'http://a0.twimg.com/profile_images/3608605926/71036b2e9d4deff52fdacd8196c40ce5_normal.png', 'id_str': u'14375609'},
	'2': {'auth_type': 'twitter', 'fullname': 'Brad Burnham', 'username': u'bradusv', 'screen_name': u'bradusv', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/52435733/bio_brad_normal.jpg', 'profile_image_url': u'http://a0.twimg.com/profile_images/52435733/bio_brad_normal.jpg', 'id_str': u'7410742'},
	'19': {'auth_type': 'twitter', 'fullname': 'Brittany Laughlin', 'username': u'br_ttany', 'screen_name': u'br_ttany', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/1217456552/theoffice_normal.JPG', 'profile_image_url': u'http://a0.twimg.com/profile_images/1217456552/theoffice_normal.JPG', 'id_str': u'45452822'},
	'12': {'auth_type': 'twitter', 'fullname': 'Christina Cacioppo', 'username': u'christinacaci', 'screen_name': u'christinacaci', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/1043543563/temp_normal.jpg', 'profile_image_url': u'http://a0.twimg.com/profile_images/1043543563/temp_normal.jpg', 'id_str': u'29294520'},
	'13': {'auth_type': 'twitter', 'fullname': 'Gary Chou', 'username': u'garychou', 'screen_name': u'garychou', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/3292748896/a94514170806ebf29c2f481023217967_normal.jpeg', 'profile_image_url': u'http://a0.twimg.com/profile_images/3292748896/a94514170806ebf29c2f481023217967_normal.jpeg', 'id_str': u'29058287'},
	'14': {'auth_type': 'twitter', 'fullname': 'John Buttrick', 'username': u'johnbuttrick', 'screen_name': u'johnbuttrick', 'profile_image_url_https': u'https://si0.twimg.com/sticky/default_profile_images/default_profile_2_normal.png', 'profile_image_url': u'http://a0.twimg.com/sticky/default_profile_images/default_profile_2_normal.png', 'id_str': u'314817239'},
	'8': {'auth_type': 'twitter', 'fullname': 'Eric Friedman', 'username': u'ericfriedman', 'screen_name': u'ericfriedman', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/1787982531/EricFriedman_headshot_normal.jpg', 'profile_image_url': u'http://a0.twimg.com/profile_images/1787982531/EricFriedman_headshot_normal.jpg', 'id_str': u'48263'},
	'6': {'auth_type': 'twitter', 'fullname': 'Andrew Parker', 'username': u'andrewparker', 'screen_name': u'andrewparker', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/378800000115288351/5971d74ecdf4f1f74ab563189786c03e_normal.jpeg', 'profile_image_url': u'http://a0.twimg.com/profile_images/378800000115288351/5971d74ecdf4f1f74ab563189786c03e_normal.jpeg', 'id_str': u'8722'},
	'4': {'auth_type': 'twitter', 'fullname': 'Charlie O\'Donnell', 'username': u'ceonyc', 'screen_name': u'ceonyc', 'profile_image_url_https': u'https://si0.twimg.com/profile_images/3285145326/3487ffc0050a17990357399562ac1eba_normal.jpeg', 'profile_image_url': u'http://a0.twimg.com/profile_images/3285145326/3487ffc0050a17990357399562ac1eba_normal.jpeg', 'id_str': u'768632'},
}

def calculate_score(votes, date_created):
    adjusted_votes = log(max(abs(votes), 1), 10)
    sign = 1
    age_factor = 45000.0 # ~12.5 hour increments
    timestamp = time.mktime(date_created.timetuple())
    score = adjusted_votes + round(sign * timestamp / age_factor)
    return score

#redis = redis.StrictRedis(host='localhost', port=6379, db=0)
redis = redis.StrictRedis.from_url('redis://rediscloud:0eAMK9S4d0Z18930@pub-redis-19035.us-east-1-1.1.ec2.garantiadata.com:19035')

f = open('/Users/zacim/Desktop/mt_entry.json', 'r')
entries = json.loads(f.read())
f.close()

for entry in entries['RECORDS']:
	if entry['entry_status'] != '2':
		continue
	if entry['entry_text_more']:
		continue

	if entry['entry_text'].startswith('<br />'):
		entry['entry_text'] = entry['entry_text'][6:]

	entry_text = entry['entry_text'].replace('\n\n', '<br/><br/>')

	d = parser.parser().parse(entry['entry_authored_on'])
	score = calculate_score(1, d)
	u = User(**users[str(entry['entry_author_id'])])
	p = Post(
			user=u,
			title=entry['entry_title'],
			body_raw=entry_text,
			body_html=entry_text,
			body_text=html_to_text(entry_text),
			body_truncated=sanitize.truncate(html_to_text(entry_text), 500),
			score=score,
			date_created=d,
			votes=1,
			voted_users=[VotedUser(id=u.id_str)],
			featured=True,
			date_featured=d,
		)
	p.save()
	redis.set('post:%s:votes' % p.id, 1)
	old_url = '/%i/%02i/%s.php' % (d.year, d.month, entry['entry_basename'].replace('_', '-'))
	new_url = '/%s' % p.slug

	# Verify that the old_url is correct
	request = urllib2.Request('http://www.usv.com%s' % old_url)
	request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36')
	opener = urllib2.build_opener()
	try:
		o = opener.open(request)
	except:
		print old_url
		print p.title
		print p.body_text
		sys.exit(0)

	print "{'%s': '%s'}" % (old_url, new_url)

	#redis.zadd('hot', score, p.id)
	#redis.zadd('new', time.mktime(d.timetuple()), p.id)

