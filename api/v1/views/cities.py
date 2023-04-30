#!/usr/bin/python3
"""view for cities objects that handles all default RESTFul API actions"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def states_cities(state_id):
    """ GET cities liked with state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    list_city = []
    for city in storage.all("City").values():
        if city.state_id == state_id:
            list_city.append(city.to_dict())
    return jsonify(list_city)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id(city_id):
    """GET cities id"""
    for city in storage.all("City").values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_cities(city_id):
    """DELETE state id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """post states"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    if 'name' not in request.get_json():
        abort(400, {'message': 'Missing name'})

    city = City(state_id=state_id, **data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """PUT states"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
