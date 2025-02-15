#!/usr/bin/python3
"""
Contains a python script that creates a flask blueprint
named app_views with the url prefix /api/v1/ as part of a larger
flask application
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.cities import *
