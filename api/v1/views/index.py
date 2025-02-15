#!/usr/bin/python3
"""
To be documented
"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the api
    """
    return (jsonify({'status': 'OK'}))
