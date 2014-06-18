import sys
sys.path.insert(0, '/Users/nick/dev/conversation')
import settings
import logging
from datetime import datetime, timedelta
import optparse
from lib import statsdb, postsdb

parser = optparse.OptionParser()
parser.add_option('-s', '--start',
        action="store", dest="start_date",
        help="start date", default="today")
options, args = parser.parse_args()

if options.start_date == "today":
    options.start_date = datetime.today()

start_date_str = options.start_date
start_date = datetime.strptime(start_date_str, "%m-%d-%Y")
end_date = start_date + timedelta(days=7)
count = postsdb.get_post_count_for_range(start_date, end_date)
unique_posters = postsdb.get_unique_posters(start_date, end_date)
single_post_count = 0
for user in unique_posters:
    if user['count'] == 1:
        single_post_count += 1


print "Week starting %s" % start_date_str
print "+++ %s posts" % count
print "+++ %s unique posters" % len(unique_posters)
print "+++ %s one-time posters" % single_post_count
