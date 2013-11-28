import os

os.environ['ACTIVE_THEME'] = "usv"

#
# DEV DB
#
#os.environ['MONGODB_URL'] = "localhost"
#os.environ['DB_NAME'] = "usv"
#
#os.environ['MONGODB_URL'] = "mongodb://usv_dev:TheDevDB@ds047198.mongolab.com:47198/usv_dev_2"
#os.environ['DB_NAME'] = "usv_dev_2"

#
# PROD DB
#
os.environ['MONGODB_URL'] = 'mongodb://heroku:cC4MKy5YYanQy6vH@chang.mongohq.com:10032/app18119720'
os.environ['DB_NAME'] = 'app18119720'

#
# ENVIRONMENT.  dev for local DB.  test for dev.usv.com db
#
os.environ['ENVIRONMENT'] = "prod"

os.environ['BASE_URL'] = "http://www.usv.com"
os.environ['COOKIE_SECRET'] = "5atEhl8WPsfA3OEmBZChGbDANDddXyKEX5gUnqKjDzIA"

os.environ['DISQUS_PUBLIC_KEY'] = "4ckXraUg1DUNC8D7nw9eFqqeTVkco5pKEaq6WsRH44psJME3RqswbwK0CeP1OSyb"
os.environ['DISQUS_SECRET_KEY'] = "saxy2rEv0cLTnGkQNFD5Q0u3Rlet8XTXTi29G2ADxysD9S7etIijmPBpXEs0xvd2"
os.environ['DISQUS_SHORT_CODE'] = "usvbeta"

os.environ['TWITTER_CONSUMER_KEY'] = "jor1WPC4w5jpKDvx4njUqg"
os.environ['TWITTER_CONSUMER_SECRET'] = "KzItojLqPQfGGnIjBzgG8QV981gCRtaENV80TzdIcI"