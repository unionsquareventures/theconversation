import urllib
import json
from mongo import db
import pymongo


''' Returns all jobs, default sorted by date added '''
def get_all():
	return list(db.gmail.find(sort=[('name', pymongo.ASCENDING)]))

''' Returns account info for an email address '''
def get_by_account(account):
	return db.gmail.find_one({'account': account})

''' Returns account info for a USVer name '''
def get_by_name(name):
	return db.gmail.find_one({'name': name})