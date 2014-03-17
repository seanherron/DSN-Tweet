import os
import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from bs4 import BeautifulSoup
import urllib2

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

@app.route('/')
def index():
    return "Hello from Craft Status"
    
def import_status():
    print "import status!"
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
        
        print craft_name
        hello = craft_status.query.filter_by(craft_name==craft_name, updated > datetime.datetime.now() - datetime.timedelta(hours=24)).first()
        print hello
        
        #status = craft_status(craft_name = craft_name, craft_friendly_name = craft_friendly_name, updated=updated, uplegRange=uplegRange, downlegRange = downlegRange, rtlt=rtlt)
        #db.session.add(status)
        
        #db.session.commit()
    
if __name__ == '__main__':
    import_status()
    