from mongo import db
import pymongo
import json
import logging
from datetime import datetime

from lib import postsdb, userdb

import settings
import urllib2
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
    subject = "Top USV.com posts for %s" % datetime.today().strftime("%a %b %d, %Y")
    body_html = "<p>Here are the posts with the mosts for today:</p><hr />"
    email_name = "Daily %s" % datetime.today().strftime("%a %b %d, %Y")

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

    # create the email
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

    return result

#
# Setup Email List
#
def setup_email_list():
    email_sent = False
    recipients = userdb.get_newsletter_recipients()
    email_name = "Daily %s" % datetime.today().strftime("%a %b %d, %Y")

    # =====
    # 1) create a "list" for today's email
    # POST https://api.sendgrid.com/api/newsletter/lists/add.json
    # @list (list name)
    api_link = 'https://api.sendgrid.com/api/newsletter/lists/add.json'
    params = {
            'list': email_name
    }
    result = do_api_request(api_link, method='POST', params=params)

    # 4) add everyone from our recipients list to the sendgrid list
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

#
# Add the newly created list to the email
#
def add_list_to_email():
    email_name = "Daily %s" % datetime.today().strftime("%a %b %d, %Y")
    # 3) Add your list to the email
    # POST https://api.sendgrid.com/api/newsletter/recipients/add.json
    # @list (name of the list to assign to this email) @name (name of the email)
    api_link = 'https://api.sendgrid.com/api/newsletter/recipients/add.json'
    params = {
            'list': email_name,
            'name': email_name,
    }
    result = do_api_request(api_link, method="POST", params=params)
    print result

#
# Actually Send it
#
def send_email():
    email_name = "Daily %s" % datetime.today().strftime("%a %b %d, %Y")
    # 5) send the email
    # POST https://api.sendgrid.com/api/newsletter/schedule/add.json
    # @email (created in step 3)
    api_link = 'https://api.sendgrid.com/api/newsletter/schedule/add.json'
    params = {
            'email': email,
            'name': "Daily %s" % datetime.datetime.today().strftime("%a %b %d, %Y")
    }
    result = do_api_request(api_link, 'POST', params=params)
    return result

#
# Add a daily email to the log
#
def log_daily_email(email, recipient_usernames):
    data = {
            'timestamp': datetime.now(),
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
