#!/bin/env python3

from flask import Blueprint

from ..models import User, Post, Comment
from .. import db
from ..utils.json_common import json_load, json_return
from flask import render_template, redirect, request, url_for, flash, abort, current_app
from flask.ext.login import login_required, current_user

comments = Blueprint('comments', __name__)


@comments.route('/submit', methods=['POST'])
def submit_comment():
    data = json_load()
    post = Post.query.get(data['postid'])
    if not post:
        return json_return(False, msg="post does not exist")
    comment = Comment(comment_body=data['content'],
                      comment_author=data['author'],
                      post_id=data['postid'])
    db.session.add(comment)
    db.session.commit()
    return json_return(True, "submit comment success!");

@comments.route('/delete', methods=['POST'])
def delete_comment():
    data = json_load()
    comment = Comment.query.get(data['commentid'])
    if not comment:
        return json_return(False, "comment does not exist")
    db.session.delete(comment)
    db.session.commit()
    return json_return(True, "delete success!")

@comments.route('/edit', methods=['POST'])
def edit_comment():
    data = json_load()
    comment = Comment.query.get(data['commentid'])
    if not comment:
        return json_return(False, "comment does not exist")
    comment.comment_body=data['content']
    db.session.add(comment)
    db.session.commit()
    return json_return(True, "modify success!")


