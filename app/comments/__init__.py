#!/bin/env python3

from flask import Blueprint

comments = Blueprint('comments', __name__)

from . import views
