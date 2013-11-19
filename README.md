USV
======

USV.com community site.

Built with:

 * Python / [Tornado](http://tornadoweb.org)
 * [Mongodb](http://www.mongodb.com/)
 * [Disqus](http://disqus.com/api/docs/)
 * [Twitter](http://dev.twitter.com)
 * [Hackpad](https://hackpad.com/Hackpad-API-v1.0-k9bpcEeOo2Q)
 * [Sendgrid](http://sendgrid.com/docs/API_Reference/)
 * [Google API](https://developers.google.com/url-shortener/v1/getting_started)
 * [Bitly](https://github.com/bitly/bitly-api-python)

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

Installation
------------

* start a local instance of mongo

./mongod

* Start the web server:

python tornado_server.py

* Site should be viewable at http://localhost:8001

Documentation
------------

Basic business logic, organization details, and other documentation can be found in the documentation folder.