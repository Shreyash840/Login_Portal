from datetime import datetime
from Login_app import db


class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(25))
    registered_timestamp = db.Column(db.DateTime, default=datetime.now)
    last_login_timestamp = db.Column(db.DateTime, default=datetime.now)
