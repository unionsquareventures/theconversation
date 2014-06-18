from mongo import db
import postsdb

import settings
import urllib2
import datetime

# For stats, we have two collections:
# "daily" and "weekly"
# a document in each collection is a day or a week
# each collection looks like:

"""
{
        _id: ...,
        timestamp: Date(),
        metric1: 0
}

"""

def insert_stat(stat="foo", value="Bar", timescale="day"):
    #
    # We expect that stats will be added on a daily basis
    # Via a cron job, at 12:01 am
    #

    # handle time -- create timestamp for start of preceding day at 12:00am
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)
    yesterday = today - datetime.timedelta(days=1)

    # calculate the appropriate monday -- for week beginning that monday
    dow = yesterday.weekday()
    monday = yesterday - datetime.timedelta(days=dow)

    # setup daystats object
    daystats = db.stats.daily.find_one({'timestamp': yesterday})
    if daystats:
        daystats[stat] = value
    else:
        daystats = {
                'timestamp': yesterday,
                stat: value
        }

    # upsert the daily document
    db.stats.daily.update({'timestamp': yesterday }, daystats, upsert=True)

    # upsert the weekly document.
    sumkey = "%s.sum" % stat
    countkey = "%s.count" % stat
    db.stats.weekly.update( { 'timestamp': monday }, { '$inc': { sumkey : value, countkey : 1 } }, upsert=True )
