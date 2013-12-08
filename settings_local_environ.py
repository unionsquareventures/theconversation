import os
#
# DEV DB
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
os.environ['ENVIRONMENT'] = "test"

os.environ['BASE_URL'] = "localhost:8001"
os.environ['COOKIE_SECRET'] = "5atEhl8WPsfA3OEmBZChGbDANDddXyKEX5gUnqKjDzIA"

os.environ['DISQUS_PUBLIC_KEY'] = "BJ83AEsDt1F9gjVD6DR6BepFbAToZkNHrDna7mWxRIEn5uNGzB4QH4hdbUHphsUy"
os.environ['DISQUS_SECRET_KEY'] = "BE2SlUCB7oxLb73ppE9hKkcThwdV2kIiHN8STRbPQCKLsOIPiMopBBfQVtiEXoC9"
os.environ['DISQUS_SHORT_CODE'] = "usvdev"

os.environ['TWITTER_CONSUMER_KEY'] = "jor1WPC4w5jpKDvx4njUqg"
os.environ['TWITTER_CONSUMER_SECRET'] = "KzItojLqPQfGGnIjBzgG8QV981gCRtaENV80TzdIcI"