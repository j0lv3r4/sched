from flask import Flask, render_template, Blueprint, session, redirect, \
        request, url_for, flash
from app import app
from app import db
from app.models import User, Post

mod = Blueprint('admin', __name__, url_prefix='/admin')

@mod.route('/users', methods=['GET'])
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@mod.route('/posts', methods=['GET'])
def admin_posts():
    posts = Post.query.all()
    return render_template('admin_posts.html', posts=posts)
