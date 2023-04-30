#!/usr/bin/python3
"""FLASK APP USING RESTful API"""
from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ a handler for 404 errors """
    return ((jsonify({"error": "Not found"})))


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
