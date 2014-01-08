from mongo import db
import pymongo

from lib import postsdb, userdb

import settings
import urllib2
import datetime
import requests

# track emails sent to users

"""
{
	_id: ...,
	timestamp: Date(),
	subject: "",
	body: "",
	recipients: []
}

"""
	
#
# Construct a daily email
#
def construct_daily_email(slugs):
	from_email = "web@usv.com"
	subject = "Top USV.com posts for %s" % datetime.datetime.today().strftime("%a %b %d, %Y")
	body_html = "<p>Here are the posts with the mosts for today:</p><hr />"
	
	posts = []
	for slug in slugs:
		post = postsdb.get_post_by_slug(slug)
		posts.append(post)
	
	for post in posts:
		post['url'] = post.get('url', '')
		source = post.get('domain', '')
		body_html += "<p><b><a href='%s'>%s</a></b> (%s)</p>" % (post['url'], post['title'], source)
		body_html += "<p>posted by @<a href='http://%s/user/%s'>%s</a> | %s comments | %s &uarr;</p>" % (settings.get('base_url'), post['user']['username'], post['user']['username'], post['comment_count'], post['votes'])
		body_html += "<p>%s</p>" % post['body_html']
		body_html += "<p>discussion: <a href='http://%s/posts/%s'>http://%s/posts/%s</a></p>" % (settings.get('base_url'), post['slug'], settings.get('base_url'), post['slug'])
		body_html += "<hr />"
	
	email = {
		'from': from_email,
		'subject': subject,
		'body_html': body_html
	}
	return email

#
# Send a daily email
#
def send_daily_email(email):
	recipients = userdb.get_newsletter_recipients()
	recipient_usernames = [r['user']['username'] for r in recipients]
	for user in recipients:
		# send email
		if settings.get('environment') != "prod":
			print "If this were prod, we would have sent email to %s" % user['email_address']
		else:
			requests.post(
				"https://sendgrid.com/api/mail.send.json",
				data={
					"api_user":settings.get('sendgrid_user'),
					"api_key":settings.get('sendgrid_secret'),
					"from": email['from_email'],
					"to": user['email_address'],
					"subject": email['subject'],
					"html": email['body_html']
				},
				verify=False
			)
	# log it
	log_daily_email(email, recipient_usernames)

#
# Add a daily email to the log
#
def log_daily_email(email, recipient_usernames):
	data = {
		'timestamp': datetime.datetime.now(),
		'subject': email['subject'],
		'body': email['body_html'],
		'recipients': recipient_usernames
	}
	db.email.daily.insert(data)
	
#
# Get log of daily emails
#
def get_daily_email_log():
	return list(db.email.daily.find({}, sort=[('timestamp', pymongo.DESCENDING)]))