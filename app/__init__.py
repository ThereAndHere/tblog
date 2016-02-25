#!/bin/env python3

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
pagedown = PageDown()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .views.user import user as user_blueprint
    from .views.posts import posts as posts_blueprint
    from .views.main import main as main_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(posts_blueprint, url_prefix='/posts')
    app.register_blueprint(main_blueprint)

    return app
