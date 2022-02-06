#!/usr/bin/python3
"""
View for Places that handles all RESTful API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ returns list of all Place objects linked to a given City """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_all = []
    for place in city.places:
        if place.city_id == city_id:
            places_all.append(place.to_dict())
    return jsonify(places_all)


@app_views.route('/places/<place_id>',  methods=['GET'], strict_slashes=False)
def places_get(place_id):
    """ Return the place and it ID. Handles GET method """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place = place.to_dict()
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a place"""
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    else:
        storage.delete(places)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_places(city_id):
    """Creates a place. Handles POST method"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    place = place.to_dict()
    return jsonify(place), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_put(place_id):
    """ handles PUT method """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key in ignore_keys:
            pass
        else:
            setattr(place, key, value)
    storage.save()
    dic_place = place.to_dict()
    return jsonify(dic_place), 200
