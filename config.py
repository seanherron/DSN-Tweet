import os
import datetime

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

DSN_STATUS_FILE_URL = 'http://eyes.nasa.gov/dsn/data/dsn.xml?r=%s' % datetime.datetime.now()
SPACECRAFT_MAP_URL = 'http://eyes.nasa.gov/dsn/config.xml'