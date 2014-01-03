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

''' Returns highest intro id. Used for creating
	new intro '''
def get_highest_id():
	return db.brittbot.find()

