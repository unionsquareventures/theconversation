# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
import settings
import requests
import logging
from lib import emailsdb
import csv


''''
recipients = userdb.get_newsletter_recipients()
csvfile = open('daily_emails.csv', 'wb')
writer = csv.writer(csvfile)
for user in recipients:
	data = [
		user['user']['username'],
		user['email_address']
	]
	writer.writerow(data)
csvfile.close()
'''

email = emailsdb.construct_daily_email(['innovation-under-austerity-eben-moglens-call-to-arms-from-freedom-to-connect'])

send = emailsdb.send_daily_email(email)