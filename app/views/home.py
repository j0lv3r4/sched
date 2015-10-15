from flask import Flask, render_template, Blueprint, session, redirect, \
        request, url_for, flash
from flask_oauthlib.client import OAuth
from app import app

mod = Blueprint('home', __name__)

# Routes
@mod.route('/')
def home():
    if 'twitter_user' in session:
        return redirect(url_for('user.profile'))
    else:
        return render_template('index.html')

