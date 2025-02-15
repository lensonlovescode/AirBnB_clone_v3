#!/usr/bin/python3
"""
Contains app route for /status in the blueprint app_views
It returns an okay status code for the api
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the api
    """
    return (jsonify({'status': 'OK'}))
