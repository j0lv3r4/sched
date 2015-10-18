from . import db
from flask.ext.sqlalchemy import SQLAlchemy

role_users = db.Table('role_users', 
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    # password = db.Column(db.String(255))
    # active = db.Column(db.Boolean())
    # confirmed_at = db.Column(db.DateTime())
    posts = db.relationship('Post', backref='user',
            lazy='dynamic')
    schedule_times = db.Column(db.String(500))
    oauth_token = db.Column(db.String(255))
    oauth_token_secret = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=role_users, 
            backref=db.backref('users', lazy='dynamic'))

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    title = db.Column(db.String(140))
    description = db.Column(db.String(255))
    long_link = db.Column(db.String(500))
    short_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
