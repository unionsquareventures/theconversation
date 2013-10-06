import settings
from mongoengine import *
mongodb_db = urlparse(settings.mongodb_url).path[1:]
connect(mongodb_db, host=settings.mongodb_url)

class Staffer(Document):
	name = StringField(max_length=1000)
	title = StringField(max_length=1000)
	bio = StringField(max_length=1000)
	twitter_handle = StringField(max_length=1000)
	website_url = StringField(max_length=1000)

	def editlink(self):
		return ""