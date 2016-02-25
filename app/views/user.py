#!/bin/env python3
from flask import Blueprint

from ..models import User
from .. import db
from ..forms.login_form import LoginForm
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user

user = Blueprint('user', __name__)



@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(user_name=form.username.data).first()
        if u is not None and u.verify_password(form.password.data):
            login_user(u, form.remember_me.data)
            u.ping()
            return redirect(request.args.get('next') or url_for('user.login'))
        flash('Invalid username or password');
    return render_template('user/login.html', form=form)

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))
