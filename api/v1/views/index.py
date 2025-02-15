#!/usr/bin/python3
"""Index route for API status"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", methods=["GET"])
def status():
    """Returns API status"""
    return jsonify({"status": "OK"})
