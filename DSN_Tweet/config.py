import os
import datetime

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

DSN_STATUS_FILE_URL = 'http://eyes.nasa.gov/dsn/data/dsn.xml?r=%s' % datetime.datetime.now()
SPACECRAFT_MAP_URL = 'http://eyes.nasa.gov/dsn/config.xml'

TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET = os.environ['TWITTER_API_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']