Deploying to Heroku
====================

1. Install the [Heroku Toolbelt](http://toolbelt.heroku.com) to start, then follow their 'Getting Started' instructions, including logging in the first time:

```
% heroku login
Enter your Heroku credentials.
Email: youremail@example.com
Password:
Could not find an existing public key.
Would you like to generate one? [Yn]
Generating new SSH public key.
Uploading ssh public key /Users/you/.ssh/id_rsa.pub
```

1. On your local machine, grab the code:

```
% git clone git@github.com:unionsquareventures/theconversation.git
Cloning into 'theconversation'...
remote: Counting objects: 14424, done.
remote: Compressing objects: 100% (5626/5626), done.
remote: Total 14424 (delta 8513), reused 14288 (delta 8400)
Receiving objects: 100% (14424/14424), 48.10 MiB | 50.00 KiB/s, done.
Resolving deltas: 100% (8513/8513), done.
Checking connectivity... done
```

1. Move into the app directory:

```
% cd theconversation
```

1. Create a heroku app:

```
% heroku app:create --name <pick-a-name>
Creating <your-app-name>... done, stack is cedar
http://<your-app-name>.herokuapp.com/ | git@heroku.com:<your-app-name>.git
Git remote heroku added
```

Visit your [Heroku Dashboard](http://id.heroku.com) and check that your new app is there.

1. You'll need to add a heroku add-on for your mongodb database.  From the "Resources" view of your app, click "Get Add-ons" from the bottom of the list, and choose a Mongodb provider from the "Data Stores" section.  We've had good experience with MongoHQ and Mongolab.  

Adding this database will automatically add a heroku config variable to our deployment, which we'll use in a minute.

1. Back in your terminal, look up the mongodb connection string that heroku just created for you:

```
% heroku config --app <your-app-name>
=== <your-app-name> Config Vars
MONGOLAB_URI:  mongo://<username>:<pw>@<host>.<provider-domain>:<port>/<db-name>
```

We'll use the value saved here for MONGOLAB_URI in a sec.  In the meantime, you'll also want to rename it within your heroku app, since we use the more generic MONGODB_URL:

```
% heroku config:set MONGODB_URL=<value-from-last-step>
Setting config vars and restarting <your-app-name>... done, v793
```

1. Create your local settings file.  Since we are targeting heroku for deployment, we want to make sure our local build environment handles config variables in a way that works for heroku.  Heroku suggests using a .env file and their Foreman deployment app for this, but we've set things up a bit differently.  We use a local settings file called settings_local_environ.py, which stores our local development settings.  Doing it this way allows us to use Tornado's logging.info() for debugging, which you can't do with Foreman.  Phew.

```
% touch settings_local_environ.py
```
1. In the text editor of your choice, open settings_local_environ.py and add the following:

```
import os

# connection string for your mongodb instance.
os.environ['MONGODB_URL'] = "<as-retreived-in-prior-step>"
os.environ['DB_NAME'] = "<your-db-name>"

# Environment -- use "dev" for local development; "test" for staging, "prod" for production
os.environ['ENVIRONMENT'] = "dev"

os.environ['BASE_URL'] = "localhost:8001"
os.environ['COOKIE_SECRET'] = "<generate-a-random-cookie-secret>"

os.environ['DISQUS_PUBLIC_KEY'] = "<disqus-public-key>"
os.environ['DISQUS_SECRET_KEY'] = "<disqus-secret-key>"
os.environ['DISQUS_SHORT_CODE'] = "<disqus-site-name>"

os.environ['TWITTER_CONSUMER_KEY'] = "<twitter-consumer-key>"
os.environ['TWITTER_CONSUMER_SECRET'] = "<twitter-consumer-secret>"
```

Note that noth the twitter and disqus credentials should gathered as per the README.

1. Save the file and run the server:
```
% python tornado_server.py
INFO:root:starting tornado_server on 0.0.0.0:8001
```

(this assumes you have all the proper requirements installed as per requirements.txt)

Voila!

Now you can test locally and see if things work.  Assuming they do, push to heroku:

```
% git push heroku master
```

(assuming that your remote is named "heroku", which it may or may not be.

Voila again!





 
