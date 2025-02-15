#!/usr/bin/python3
"""
To be documented
"""
from flask import Blueprint, jsonify
from api.v1.views.index import *

app_views = Blueprint('app_views', url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the api
    """
    return (jsonify({'status': 'OK'}))
