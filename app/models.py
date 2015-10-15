from . import db
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
        UserMixin, RoleMixin

role_users = db.Table('roles_users', 
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.STring(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    posts = db.relationship('Post', backref='user',
            lazy='dynamic')
    roles = db.relationship('Role', secondary=roles_users, 
            backref=db.backref('users', lazy='dynamic'))

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    title = db.Column(db.String(140))
    description = db.Column(db.String(255))
    long_link = db.Column(db.string(500))
    short_link = db.Column(db.string(255))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastorea)
