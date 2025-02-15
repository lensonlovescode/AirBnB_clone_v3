#!/usr/bin/python3
"""
Creates a flask app comprising many flask blueprints
as part of api building
"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_context
def close_db_session(exception=None):
    """
    Closes the database session
    """
    storage.close()


if __name__ == '__main__':

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default=5000))
    app.run(host=host, port=port, threaded=True)
