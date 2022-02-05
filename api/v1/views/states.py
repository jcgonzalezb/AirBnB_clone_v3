#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """ Retrieves a list of all State object"""
    states_all = []
    states = storage.all("State").values()
    for state in states:
        states_all.append(state.to_dict())

    return jsonify(states_all)


@app_views.route('/states/<state_id>',  methods=['GET'])
def state_get(state_id):
    """ Handles GET method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    """Deletes a state"""
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    else:
        storage.delete(states)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ Creates a state """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    elif 'name' not in data.keys():
        abort(400, "Missing name")
    else:
        new_state = State(**data)
        storage.new(new_state)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id=None):
    """ handles PUT method """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200
