#!/usr/bin/python3
"""
View for City that handles all RESTful API actions
"""
from models import city, storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def list_cities_by_states(state_id):
    """ Retrieves a list of all City objects of a State. """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities_all = []
    for city in state.cities:
        cities_all.append(city.to_dict())

    return jsonify(cities_all), 200


@app_views.route('/cities/<city_id>',  methods=['GET'],
                 strict_slashes=False)
def city_get(city_id):
    """ Retrieves a City object. Handles GET method """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """Deletes a city"""
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    else:
        storage.delete(cities)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a city. Handles POST method """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    elif 'name' not in data:
        abort(400, "Missing name")
    else:
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id=None):
    """ Updates a City. Handles PUT method """

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)

    obj.name = data['name']
    storage.save()
    res = obj.to_dict()
    return jsonify(res), 200
