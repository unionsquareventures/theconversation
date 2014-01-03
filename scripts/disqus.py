# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/nick/dev/conversation')
import settings
import requests


api_link = 'https://disqus.com/api/3.0/threads/remove.json'
info = {
	'api_secret': settings.get('disqus_secret_key'),
	'forum': settings.get('disqus_short_code'),
	'thread': 2088531932,
	'access_token': "0a75d127c53f4a99bd853d721166af14"
}
r = requests.post(api_link, params=info)
print r.json()