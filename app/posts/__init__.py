#!/bin/env python3

from flask import Blueprint

posts = Blueprint('posts', __name__)

from . import views
