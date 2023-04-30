#!/usr/bin/python3
"""
Flask app
"""
from api.v1.views import app_views
from flask import Flask, render_template, jsonify
from models import storage
from models.state import State
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status', methods=['GET'])
def status():
    """status"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'])
def stas():
    """ an endpoint that retrieves the number of each objects by type"""
    dict_ = {}
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    for i in range(len(names)):
        dict_[names[i]] = storage.count(classes[i])

    return jsonify(dict_)
