#!/bin/env python3

import os
from flask import Blueprint

#from . import posts
from ..models import User, Post
from .. import db
from ..utils.upload_checker import UploadChecker
from flask import render_template, redirect, request, url_for, flash, abort, current_app
from flask import json, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename
import imghdr
from io import BufferedReader

posts = Blueprint('posts', __name__)

@posts.route('/')
def list_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.post_timestamp.desc()).paginate(
            page, per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False)
    posts = pagination.items
    return render_template('posts/list_posts.html', posts=posts, pagination=pagination)

@posts.route('/new', methods=['POST', 'GET'])
@login_required
def new_post():
    return render_template('posts/new_post.html')
'''
    form = PostEditForm()
    if form.validate_on_submit():
        post = Post(post_title=form.title.data,
                    post_body=form.body.data,
                    user=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.show_post', id=post.post_id))
    return render_template('posts/edit_post.html', form=form)
    '''

@posts.route('/submit', methods=['POST'])
@login_required
def submit_post():
    data = json.loads(request.form.get('data'))
    post = Post(post_title=data['title'],
                post_body=data['content'],
                post_link=data['link'],
                user=current_user._get_current_object())
    db.session.add(post)
    db.session.commit()
    return 'Submit Success'

@posts.route('/submit/<int:id>', methods=['POST'])
@login_required
def submit_post_by_id(id):
    post = Post.query.get(id)
    if post:
        data = json.loads(request.form.get('data'))
        post.post_title = data['title']
        post.post_body = data['content']
        post.post_link = data['link']
        db.session.add(post)
        return 'Submit Success'
    return "Post doesn't exits"

@posts.route('/edit', methods=['POST'])
@login_required
def edit_post_by_post():
    data = json.loads(request.form.get('data'))
    id = data['id']
    return url_for('posts.edit_post', id=id)



@posts.route('/edit/<int:id>', methods=['GET'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if int(current_user.get_id()) != post.user_id:
        abort(403)
    return render_template('posts/new_post.html', post=post)
    '''
    form = PostEditForm()
    if form.validate_on_submit():
        post.post_title = form.title.data
        post.post_body = form.body.data
        db.session.add(post)
        flash('Update post success!')
        return redirect(url_for('posts.show_post', id=post.post_id))
    form.title.data = post.post_title
    form.body.data = post.post_body
    return render_template('posts/edit_post.html', form=form)
    '''

@posts.route('/detail/<int:id>', methods=['POST', 'GET'])
def show_post(id):
    post = Post.query.get_or_404(id)
    post.post_readcnt += 1
    return render_template('posts/post.html', post=post)

@posts.route('/detail/<string:link>', methods=['POST', 'GET'])
def show_post_by_link(link):
    post = Post.query.filter_by(post_link=link).first()
    if not post:
        abort(404)
    post.post_readcnt += 1
    return render_template('posts/post.html', post=post)

@posts.route('/upload', methods=['POST'])
@login_required
def upload_file():
    f = request.files['0']
    uc = UploadChecker(f)
    fname = uc.get_filename()
    fpath = os.path.join(current_app.config['UPLOAD_FOLDER'], fname)
    f.save(fpath)
    return jsonify(success=True,
                   path=[url_for('static', filename="uploads/"+fname)])

@posts.route('/delete', methods=['POST'])
@login_required
def delete_post():
    data = json.loads(request.form.get('data'))
    post = Post.query.get(data['id'])
    if post:
        db.session.delete(post)
        db.session.commit()
        return "Post deleted"
    return "Post doesn't exits"


