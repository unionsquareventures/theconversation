import urllib
import json
from mongo import db
import pymongo

"""
{
    "_id": {
        "$oid": "52951ad2bf814a94370317a0"
    },
    "city": "San Francisco",
    "position": "Operations", # Job title determined by Gary's parse_position
    "date": "Tue, 26 Nov 2013 03:07:57 GMT",
    "latitude": 37.774727,
    "url": "http://www.indeed.com/rc/clk?jk=d16f4523a3212c0b&qd=9FdQIF7yu...",
    "jobtitle": "TV Production Associate",
    "company": "Twitter",
    "formattedLocationFull": "San Francisco, CA",
    "longitude": -122.41758,
    "onmousedown": "indeed_clk(this, '842');",
    "snippet": "use tools such as the new Mirror API...", 
    "source": "Twitter",
    "state": "CA",
    "sponsored": false,
    "country": "US",
    "formattedLocation": "San Francisco, CA",
    "jobkey": "d16f4523a3212c0b", #Unique job id from Indeed
    "id": 349,
    "expired": false,
    "formattedRelativeTime": "19 hours ago"
}
"""

''' Returns all intros '''
def get_all():
	return list(db.brittbot.find())

''' Saves an intro to the database. Intro arg is a dict.
	Can be brand new or updating existing. '''
def save_intro(intro):
	if 'id' not in intro.keys() or intro['id'] == '':
	    # need to create a new intro id
	    intro['id'] = int(db.brittbot.count() + 1)
	return db.brittbot.update({'id':intro['id']}, intro, upsert=True)

def remove_intro(intro):
	if 'id' in intro.keys():
		return db.brittbot.remove({'id':intro['id']})

