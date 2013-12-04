USV
======

USV.com community site.

Built with:

 * Python / [Tornado](http://tornadoweb.org)
 * Mongodb and [Mongoengine](http://mongoengine.org)
 * [Redis](http://redis.io)
 * [Disqus](http://disqus.com)
 * [Twitter](http://dev.twitter.com)
 * Deployed at www.usv.com using [Heroku](http://heroku.com)
 * Performance / security by [Cloudflare](http://cloudflare.com)
 
Installation
------------

 * Install the [Heroku toolbelt](https://toolbelt.heroku.com/)
 * Before installing, create a .env file in the root directory, and set the following config variables:

		MONGODB_URL=mongodb://your-mongo-url
   		REDIS_URL=redis://your-redis-url

 * Create a [virtualenv](https://github.com/pypa/virtualenv), activate it, and run 

 		pip install -r requirements.txt

 * Start the web server, using [Foreman](https://devcenter.heroku.com/articles/procfile#developing-locally-with-foreman):

 		foreman start

 * Site should be viewable at http://0.0.0.0:5000

