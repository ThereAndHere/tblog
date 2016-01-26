#!/bin/env python3

from flask import Blueprint

user = Blueprint('user', __name__)

from . import views
