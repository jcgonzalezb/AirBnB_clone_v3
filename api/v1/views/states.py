#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/states',methods=['GET'], strict_slashes=False)
def list_states():
    """ Retrieves a list of all State object"""
    states_all = []
    states = storage.all("States").values()
    for state in states:
        states_all.append(state.to_dict())
    
    return jsonify(states_all)

@app_views.route('/states/<state_id>',  methods=['GET'])
def state_get(state_id):
    """ Handles GET method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state = state.to_json()
    return jsonify(state)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    """Deletes a state"""
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

@app_views.route('/states/<state_id>', methods=['POST'])
def state_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_json()
    return jsonify(state), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ handles PUT method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            state.bm_update(key, value)
    state.save()
    state = state.to_json()
    return jsonify(state), 200
