import os
import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from bs4 import BeautifulSoup
import urllib2
import twitter

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True

db = SQLAlchemy(app)

class craft_status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    craft_name = db.Column(db.String(180))
    craft_friendly_name = db.Column(db.String(180))
    updated = db.Column(db.DateTime, default=datetime.datetime.now())
    uplegRange = db.Column(db.String(180))
    downlegRange = db.Column(db.String(180))
    rtlt = db.Column(db.String(180))
    
    def __init__(self, craft_name, craft_friendly_name, updated, uplegRange, downlegRange, rtlt):
        self.craft_name = craft_name
        self.craft_friendly_name = craft_friendly_name
        self.updated = updated
        self.uplegRange = uplegRange
        self.downlegRange = downlegRange
        self.rtlt = rtlt
        
    def __repr__(self):
        return '<Craft Status %r %r>' % (self.craft_friendly_name, self.updated)
        
class tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    craft_status_id = db.Column(db.Integer, db.ForeignKey('craft_status.id'))
    updated = db.Column(db.DateTime, default=datetime.datetime.now())
    
    def __init__(self, craft_status_id, updated):
        self.craft_status_id = craft_status_id
        self.sent = sent
        
def init_db():
    db.create_all()

def import_status():
    dsn = BeautifulSoup(urllib2.urlopen(app.config['DSN_STATUS_FILE_URL']), "xml")
    spacecrafts = BeautifulSoup(urllib2.urlopen(app.config['SPACECRAFT_MAP_URL']), "xml")
    
    targets = dsn.find_all('target')
    for target in targets:
        craft_name = target.get('name')
        craft_friendly_name = spacecrafts.config.spacecraftMap.find("spacecraft", {"name": craft_name.lower()}).get("friendlyName")
        updated = datetime.datetime.now()
        uplegRange = target.get('uplegRange')
        downlegRange = target.get('downlegRange')
        rtlt = target.get('rtlt')
        
        status = craft_status(craft_name = craft_name, craft_friendly_name = craft_friendly_name, updated=updated, uplegRange=uplegRange, downlegRange = downlegRange, rtlt=rtlt)
        db.session.add(status)
        db.session.commit()

def twitter_update():
    def send_tweet(message):
        api = twitter.Api(
                consumer_key=app.config['TWITTER_API_KEY'],
                consumer_secret=app.config['TWITTER_API_SECRET'],
                access_token_key=app.config['TWITTER_ACCESS_TOKEN'],
                access_token_secret=app.config['TWITTER_ACCESS_TOKEN_SECRET'])
        try:
            api.PostUpdate('Test Message')
            
        
    if tweets.query.order_by(tweets.id.desc()).first():
        send_tweet('Last Tweet Detected')
    else:
        send_tweet('No Last Tweet')
    #timedelta = datetime.datetime.now() - last_tweet.sent
    #print timedelta
    
    #if last_tweet:
    #    print "Last Tweet"
    #else:
    #    print "no last weet"
    
if __name__ == '__main__':
    import_status()
    twitter_update()
    