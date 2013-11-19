from mongo import db

def save_tag(tag):
  return db.tag.update({'name':tag}, {'name':tag}, upsert=True)
