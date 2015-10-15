from flask import Flask, render_template, Blueprint, session, redirect, \
        request, url_for, flash
from flask_oauthlib.client import OAuth
from app import app


mod = Blueprint('user', __name__, url_prefix='/user')

oauth = OAuth(app)

twitter = oauth.remote_app('twitter',
        base_url='https://api.twitter.com/1.1/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        consumer_key='QRKIzox3b4SiQ2bvkl1TD8ro6',
        consumer_secret='rmdF95H5wUFkphQXWHapfKBUlNeIHqgdnZTFT1i516DItbe6uh'
    )

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@mod.route('/login')
def login():
    return twitter.authorize(callback=url_for('user.oauth_authorized', 
            next=request.args.get('next') or request.referrer or None))

@mod.route('/profile')
def profile():
    user = session['twitter_user']
    resp = twitter.request('users/show.json?screen_name={}'\
            .format(user))
    print resp.status
    if resp.status == 200:
        profile_image = resp.data['profile_image_url'].replace('_normal', '')
    return render_template('profile.html', user=user, 
            profile_image=profile_image)

@mod.route('/oauth-autorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('home.home')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    
    session['twitter_user'] = resp['screen_name']

    return redirect(next_url)
