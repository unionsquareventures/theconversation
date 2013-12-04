import settings
from markdown import markdown
import os
from mongoengine import *
from urlparse import urlparse
from custom_fields import ImprovedStringField, ImprovedURLField
mongodb_db = urlparse(settings.mongodb_url).path[1:]
connect(mongodb_db, host=settings.mongodb_url)

class Company(Document):
	meta = {
		'indexes': ['-status', 'name'],
	}
	
	id = IntField(primary_key=True)
	name = StringField(max_length=1000)
	url = StringField(max_length=1000)
	description = StringField(max_length=1000)
	logo_filename = StringField(max_length=1000, default="default.png") #to be deleted
	locations = StringField(max_length=1000)
	investment_series = StringField(max_length=1000)
	investment_year = StringField(max_length=5)
	categories = StringField(max_length=1000)
	status = StringField(max_length=1000, default="current")
	slug = StringField()
	investment_post_slug = StringField()
	
	def save(self, *args, **kwargs):
		if '_id' not in self.to_mongo():
			if self.hook_id:
				self.hook_id()
		super(Company, self).save(*args, **kwargs)

	def hook_id(self):
		counter_coll = self._get_collection_name() + 'Counter'
		counter = self._get_db()[counter_coll].find_and_modify(query={'_id': 'object_counter'},
																update={'$inc': {'value': 1}},
																upsert=True, new=True)
		id = counter['value']
		self._data['id'] = id
		
	def editlink(self):
		link = '%s/collections/company/documents/%s' % (os.environ.get('MONGODB_CLOUD_BASE_URL'), self.id)
		return link