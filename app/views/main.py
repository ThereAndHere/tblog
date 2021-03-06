#!/bin/env python3
from flask import Blueprint
from . import main
from ..models import User, Post
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Post.query.order_by(Post.post_timestamp.desc())
    return render_template('index.html', posts=posts)

@main.route('/login')
def login():
    return redirect(url_for('user.login'))
