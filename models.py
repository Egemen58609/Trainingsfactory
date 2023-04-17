
from __init__ import app, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))


class Les(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    les = db.Column(db.String(150))
    datum = db.Column(db.DateTime, nullable=False)
    users = db.relationship('Rooster')

class Rooster(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    les_id = db.Column(db.Integer, db.ForeignKey('les.id'))



from __init__ import app, db
from flask import Flask

# Create the user table in the SQLite database
with app.app_context():
    db.create_all()