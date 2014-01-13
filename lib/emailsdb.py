from mongo import db
import pymongo
import json
import logging

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
db.user_info.ensure_index('wants_daily_email')
	
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
		body_html += "<p><b><a href='%s'>%s</a></b></p>" % (post['url'], post['title'])
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
	email_sent = False
	recipients = userdb.get_newsletter_recipients()
	
	# New!  Uses the sendgrid newsletter API
	# =====
	# 1) create a "list" for today's email	
	# POST https://api.sendgrid.com/api/newsletter/lists/add.json
	# @list (list name)
	api_link = 'https://api.sendgrid.com/api/newsletter/lists/add.json'
	params = {
		'list': "Daily %s" % datetime.datetime.today().strftime("%a %b %d, %Y")
	}
	list = do_api_request(api_link, method='POST', params=params)
	print list
	if not list:
		return "Could not create List"
	
	# 2) add everyone from our recipients list to the sendgrid list
	# POST https://api.sendgrid.com/api/newsletter/lists/email/add.json
	# list=ListName  data[]={ 'email': '', 'name': '' } & data[]={ 'email': '', 'name': '' }
	api_link = 'https://api.sendgrid.com/api/newsletter/lists/email/add.json'
	data = []
	for user in recipients:
		data.append({
			'email': user.get('email_address'),
			'name': user.get('user').get('username')
		})
	params = {
		'data': json.dumps(data),
		'list': "Daily %s" % datetime.datetime.today().strftime("%a %b %d, %Y")
	}
	result = do_api_request(api_link, method='POST', params=params)
	
	# 3) create the email
	# POST https://api.sendgrid.com/api/newsletter/add.json
	# @identity (created in advance == the sender's identity), @name (of email), @subject, @text, @html
	api_link = 'https://api.sendgrid.com/api/newsletter/add.json'
	params = {
		'identity': settings.get('sendgrid_sender_identity'),
		'name': "Daily %s" % datetime.datetime.today().strftime("%a %b %d, %Y"),
		'subject': email['subject'],
		'text': '', #to do get text version,
		'html': email['body_html']
	}
	result = do_api_request(api_link, method="POST", params=params)
	
	# 4) send the email
	# POST https://api.sendgrid.com/api/newsletter/schedule/add.json
	# @email (created in step 3)
	api_link = 'https://api.sendgrid.com/api/newsletter/schedule/add.json'
	params = {
		'email': email,
		'name': "Daily %s" % datetime.datetime.today().strftime("%a %b %d, %Y")
	}
	result = do_api_request(api_link, 'POST', params=params)
	#check email sent

	if email_sent:
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
	

#####################################################
#### ACTUALLY HANDLE THE REQUESTS/RESPOSNE TO THE API
#####################################################
def do_api_request(api_link, method='GET', params={}):
	# add sendgrid user & api key
	params.update({
		'api_user': settings.get('sendgrid_user'),
		'api_key': settings.get('sendgrid_secret')
	})
	try:
		if method.upper() == 'GET':
			if len(params.keys()) > 0:
				r = requests.get(
					api_link,
					params=params,
					verify=False
				)
			else:
				r = requests.get(
					api_link,
					verify=False
				)
		else:
			r = requests.post(
				api_link,
				params=params,
				verify=False
			)
		response = r.json()
	except:
		response = {}
	if settings.get('environment') == "dev":
		logging.info("=================")
		logging.info( api_link)
		logging.info( json.dumps(params, indent=4))
		logging.info( response)
		logging.info( "=================")
	return response