#!/bin/env python3

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from ..models import User

class LoginForm(Form):
    username = StringField('username', validators=[Required(), Length(1, 64)])
    password = PasswordField('password', validators=[Required(), Length(1, 16)])
    remember_me = BooleanField('keep login')
    submit = SubmitField('Login')
