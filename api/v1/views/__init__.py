#!/usr/bin/python3
"""
To be documented
"""
from flask import Blueprint

app_views = Blueprint('app_views', url_prefix='/api/v1')

from api.v1.views.index import *
