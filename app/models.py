#!/usr/bin/env python3

from . import db
from . import login_manager
from .utils.summary_parser import SummaryParser
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin, current_app
from datetime import datetime
from markdown import markdown
import bleach

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.role_name
    

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    user_password = db.Column(db.String(128))
    user_lastseen = db.Column(db.DateTime(), default=datetime.utcnow)
    user_regtime = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.user_name

    def get_id(self):
        return str(self.user_id)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)

    def ping(self):
        self.user_lastseen = datetime.utcnow()
        db.session.add(self)

class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.Text)
    post_body = db.Column(db.Text)
    post_htmlbody = db.Column(db.Text)
    post_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_summary = db.Column(db.Text)
    post_readcnt = db.Column(db.Integer, default=0)
    post_link = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.post_title

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p', 'img']
        attrs = {'a': ['href', 'rel'],
                'img': ['src', 'alt'],
                }
        target.post_htmlbody = bleach.linkify(bleach.clean(
            markdown(value, ['pymdownx.extra', 'sane_lists'], tab_length=4),
            tags=allowed_tags, attributes=attrs, strip=True))

    @staticmethod
    def on_change_htmlbody(target, value, oldvalue, initiator):
        sp = SummaryParser(current_app.config['BLOG_SUMMARY_SIZE'])
        sp.feed(value)
        target.post_summary = sp.get_summary()


db.event.listen(Post.post_body, 'set', Post.on_change_body)
db.event.listen(Post.post_htmlbody, 'set', Post.on_change_htmlbody)

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.Text)
    comment_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comment_author = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))

    def __repr__(self):
        return '<Comment %d>' % self.comment_id

