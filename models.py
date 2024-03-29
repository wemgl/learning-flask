from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from urllib.parse import urljoin
from urllib.request import urlopen

import geocoder
import json
import ssl
import os

KEY = os.environ["GOOGLE_API_KEY"]

QUERY_URL_BASE = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password=password)


# p = Place()
# places = p.query("1600 Amphitheater Parkway Mountain View CA")
class Place(object):
    def meters_to_walking_time(self, meters):
        # 80 meters is one minute walking time
        return int(meters / 80)

    def wiki_path(self, slug):
        return urljoin("https://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlng(self, address):
        g = geocoder.google(address, key=KEY)
        if g.ok:
            return g.latlng

        return ()

    def query(self, address):
        latlng = self.address_to_latlng(address)
        if len(latlng) == 0:
            return []

        lat, lng = latlng[0], latlng[1]
        print(lat, lng)

        query_url = QUERY_URL_BASE.format(lat, lng)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        g = urlopen(query_url, context=ctx)

        results = g.read()
        g.close()

        data = json.loads(results)
        print(data)

        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {'name': name, 'url': wiki_url, 'time': walking_time, 'lat': lat, 'lng': lng}

            places.append(d)

        return places
