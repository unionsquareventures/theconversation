The Conversation
=================

Community link-sharing and discussion app, built for [USV.com](http://www.usv.com).

Built with:

 * Python / [Tornado](http://tornadoweb.org)
 * [Mongodb](http://www.mongodb.com/)
 * [Disqus](http://disqus.com/api/docs/)
 * [Twitter](http://dev.twitter.com)
 * [Hackpad](https://hackpad.com/Hackpad-API-v1.0-k9bpcEeOo2Q)
 * [Sendgrid](http://sendgrid.com/docs/API_Reference/)
 * [Google API](https://developers.google.com/url-shortener/v1/getting_started)
 * [Bitly](https://github.com/bitly/bitly-api-python)

Setup
======

Prior to installation, you'll need to do a few things:

* _Twitter_: Log into http://dev.twitter.com and set up a new application.  Note the "consumer key" and "consumer secret", which we'll need later on.
* _Disqus_: Go to http://disqus.com/api/applications/ and set up a new application.  Note the public and secret keys, which we'll use in config.  You may also need to go to http://disqus.com/admin/create/ to create a new disqus "forum", which will house the comments for your site.
* Sign up for an account at http://sendgrid.com for email delivery


Configuration
-------------

General app settings are controlled via the settings.py file. You will need to provide dev/local values for the following settings:

* 'twitter_consumer_key' : '',
* 'twitter_consumer_secret' : '',
* 'disqus_public_key': '',
* 'disqus_secret_key': '',
* 'disqus_short_code': '',
* 'sendgrid_user': '',
* 'sendgrid_secret': '',
* 'hackpad_oauth_client_id':'', 
* 'hackpad_oauth_secret':'', 
* 'hackpad_domain':'',
* 'google_api_key': '',
* 'bitly_access_token': '',

(the hackpad, google and bitly keys are optional)

Installation
------------

* start a local instance of mongo

./mongod

* OR, configure your app to use a cloud-based mongo instance, by setting "MONGODB_URL" and "DB_NAME" in settings.py

* Start the web server:

python tornado_server.py

* Site should be viewable at http://localhost:8001

Deployment to Heroku
====================
We've written up a heroku-specific deployment recipe here: https://github.com/unionsquareventures/theconversation/blob/master/documentation/heroku.md


Documentation
------------

Basic business logic, organization details, and other documentation can be found in the documentation folder.