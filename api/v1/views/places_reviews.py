#!/usr/bin/python3
"""
View for City that handles all RESTful API actions
"""
from models import city, storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def list_reviews_by_place(place_id):
    """ Retrieves a list of all review objects of a Place. """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews_all = []
    for review in place.reviews:
        reviews_all.append(review.to_dict())

    return jsonify(reviews_all), 200


@app_views.route('/reviews/<review_id>',  methods=['GET'],
                 strict_slashes=False)
def review_get(review_id):
    """ Retrieves a Review object. Handles GET method """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review = review.to_dict()
    return jsonify(review), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a review"""
    reviews = storage.get("Review", review_id)
    if reviews is None:
        abort(404)
    else:
        storage.delete(reviews)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
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
