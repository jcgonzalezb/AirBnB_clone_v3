#!/usr/bin/python3
"""
View for Amenity that handles all RESTful API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """ Retrieves a list of all Amenity objects """
    amenities_all = []
    amenities = storage.all("Amenity").values()
    for amenity in amenities:
        amenities_all.append(amenity.to_dict())

    return jsonify(amenities_all), 200


@app_views.route('/amenities/<amenity_id>',  methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object. Handles GET method """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(amenity_id=None):
    """Deletes a amenity"""
    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)
    else:
        storage.delete(amenities)
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
        new_city = Amenity(**data)
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
