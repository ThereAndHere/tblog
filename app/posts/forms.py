#!/bin/env python3

from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class PostEditForm(Form):
    title = StringField("Title", validators=[Required()])
    body = PageDownField("Markdown", validators=[Required()])
    submit = SubmitField("Publish")

