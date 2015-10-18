from flask import Flask, render_template, Blueprint, session, redirect, \
        request, url_for, flash
from flask_oauthlib.client import OAuth
from app import app, db
from app.models import Post, User


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
    if not 'twitter_user' in session:
        return redirect(url_for('home.home'))
    else:
        user = session['twitter_user']
        resp = twitter.request('users/show.json?screen_name={}'\
                .format(user))
        if resp.status == 200:
            profile_image = resp.data['profile_image_url'].replace('_normal', '')

            user_id = User.query.filter_by(username=user).first().id
            posts = Post.query.filter_by(user_id=user_id).all()
        return render_template('profile.html', user=user, 
                profile_image=profile_image, posts=posts)

@mod.route('/oauth-autorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('home.home')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    # Session
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    
    session['twitter_user'] = resp['screen_name']

    # Database entry
    user = User(username=resp['screen_name'], oauth_token=resp['oauth_token'], \
            oauth_token_secret=resp['oauth_token_secret'])

    db.session.add(user)
    db.session.commit()

    return redirect(next_url)

@mod.route('/logout', methods=['GET'])
def logout():
    session.pop('twitter_user', None)
    session.pop('oauth_token', None)
    session.pop('oauth_token_secret', None)
    return redirect(url_for('home.home'))
