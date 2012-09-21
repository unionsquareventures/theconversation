from mongoengine import *

class Question(EmbeddedDocument):
    id = IntField(primary_key=True)
    text = StringField(required=True)

    ##
    def hook_id(self):
        counter_coll = self._get_collection_name() + 'Counter'
        counter = self._get_db()[counter_coll].find_and_modify(query={'_id': 'object_counter'},
                                                                update={'$inc': {'value': 1}},
                                                                upsert=True, new=True)
        id = counter['value']
        self._data['id'] = id
    ##
    def minified_id(self):
        return minifier.int_to_base62(self.id)

    ##
    def save(self, *args, **kwargs):
        if kwargs.get('force_insert') or '_id' not in self.to_mongo():
            if self.hook_id:
                self.hook_id()
            if self.hook_date_created:
                self.hook_date_created()
        super(Post, self).save(*args, **kwargs)

