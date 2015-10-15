import os

DEBUG=True

SALT=os.getenv('SALT', '<your salt here>')
SECRET_KEY=os.getenv('SECRET_KEY', '<your secret key here>')
SECURITY_PASSWORD_HASH = os.getenv('SECURITY_PASSWORD_HASH', \
        '<your security password hash here, example: `bcrypt`>')
SECURITY_PASSWORD_SALT = SALT 

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', \
        '<your database path here>')
