#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ GET states"""
    all_states = storage.all(State).values()
    list_states = []
    for states in all_states:
        list_states.append(states.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """GET states id"""
    for state in storage.all("State").values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete(state_id):
    """DELETE state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """post states"""
    data = request.get_json()
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    if not 'name' in request.get_json():
        abort(400, {'message': 'Missing name'})

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put(state_id):
    """PUT states"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
