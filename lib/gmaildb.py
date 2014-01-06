import urllib
import json
from mongo import db
import pymongo


''' Returns all jobs, default sorted by date added '''
def get_all():
	return list(db.gmail.find())

