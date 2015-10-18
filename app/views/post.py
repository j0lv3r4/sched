from flask import Flask, render_template, Blueprint, session, redirect, \
        request, url_for, flash
from flask_oauthlib.client import OAuth
from app import app
from app import db
from app.models import User, Post
from app.views.forms import AddPostForm

mod = Blueprint('post', __name__, url_prefix='/post')

@mod.route('/add', methods=['POST', 'GET'])
def add_post():
    form = AddPostForm(request.form)

    if not 'twitter_user' in session:
        return redirect(url_for('home.home'))
    elif form.validate_on_submit():
        title = form.title.data
        user = User.query.filter_by(username=session['twitter_user']).first()
        user_id = user.id

        # user = session['twitter_user']
        
        post = Post(title=title, user_id=user_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('user.profile'))
    return render_template('add_post.html', form=form)
