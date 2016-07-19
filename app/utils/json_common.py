#!/bin/env python3
from flask import json, jsonify
from flask import request

def json_load():
    return json.loads(request.form.get('data'))

def json_return(result, message):
    return jsonify(success=result, msg=message)
