from mongo import db
import pymongo
import json
import logging

from lib import postsdb, userdb

import settings
import urllib2
import datetime
import requests
import math

from werkzeug.datastructures import MultiDict

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
	body_html += "Want to unsubscribe? Visit http://%s/user/settings" % settings.get('base_url')
	
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
	email_name = "Daily %s" % datetime.datetime.today().strftime("%a %b %d, %Y")
	
	# New!  Uses the sendgrid newsletter API
	# =====
	# 1) create a "list" for today's email	
	# POST https://api.sendgrid.com/api/newsletter/lists/add.json
	# @list (list name)
	api_link = 'https://api.sendgrid.com/api/newsletter/lists/add.json'
	params = {
		'list': email_name
	}
	result = do_api_request(api_link, method='POST', params=params)
	
	# 2) add everyone from our recipients list to the sendgrid list
	# POST https://api.sendgrid.com/api/newsletter/lists/email/add.json
	# list=ListName  data[]={ 'email': '', 'name': '' } & data[]={ 'email': '', 'name': '' }
	api_link = 'https://api.sendgrid.com/api/newsletter/lists/email/add.json'
	
	num_groups = int(math.ceil(len(recipients) / 50))
	recipient_groups = split_seq(recipients, num_groups) 

	for i, group in enumerate(recipient_groups):
		# sendgrid needs list add requests to be < 100 peole
		users = MultiDict()	
		for i, user in enumerate(group):
			if user.get('user').get('username') != "" and user.get('email_address') != "":
				users.add('data', '{"name":"%s","email":"%s"}' % (user.get('user').get('username'), user.get('email_address')))

		params = {
			'list': email_name,
			'data': users.getlist('data')
		}
	
		result = do_api_request(api_link, method='POST', params=params)
		
	# 3) create the email
	# POST https://api.sendgrid.com/api/newsletter/add.json
	# @identity (created in advance == the sender's identity), @name (of email), @subject, @text, @html
	api_link = 'https://api.sendgrid.com/api/newsletter/add.json'
	params = {
		'identity': settings.get('sendgrid_sender_identity'),
		'name': email_name,
		'subject': email['subject'],
		'text': '', #to do get text version,
		'html': email['body_html']
	}
	result = do_api_request(api_link, method="POST", params=params)
	print result
	
	'''
	# 4) Add your list to the email
	# POST https://api.sendgrid.com/api/newsletter/recipients/add.json
	# @list (name of the list to assign to this email) @name (name of the email)
	api_link = 'https://api.sendgrid.com/api/newsletter/recipients/add.json'
	params = {
		'list': email_name,
		'name': email_name,
	}
	result = do_api_request(api_link, method="POST", params=params)
	print result
	
	# 5) send the email
	# POST https://api.sendgrid.com/api/newsletter/schedule/add.json
	# @name (created in step 3)
	api_link = 'https://api.sendgrid.com/api/newsletter/schedule/add.json'
	params = {
		'name': email_name
	}
	result = do_api_request(api_link, 'POST', params=params)
	#check email sent

	# 6) Log it
	if email_sent:
		log_daily_email(email, recipient_usernames)

	'''
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
	

def split_seq(seq, num_pieces):
	newseq = []
	splitsize = 1.0/num_pieces*len(seq)
	for i in range(num_pieces):
					newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
	return newseq

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
		logging.info(r.url)
		response = r.json()
	except:
		response = {}

	logging.info("=================")
	logging.info( api_link)
	logging.info( json.dumps(params, indent=4))
	logging.info( response)
	
	logging.info( "=================")

	return response