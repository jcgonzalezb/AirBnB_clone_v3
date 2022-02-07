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
def create_review(place_id):
    """ Creates a review. Handles POST method """
    data = request.get_json(silent=True)
    place = storage.get("Place", place_id)
    user = storage.get("User", data['user_id'])
    if place is None:
        abort(404)
    elif data is None:
        abort(400, "Not a JSON")
    elif 'user_id' not in data:
        abort(400, "Missing user_id")
    elif user is None:
        abort(404)
    elif 'text' not in data:
        abort(400, "Missing text")
    else:
        data['place_id)'] = place_id
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id=None):
    """ Updates a review. Handles PUT method """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key in ignore_keys:
            pass
        else:
            setattr(review, key, value)
    storage.save()
    dic_review = review.to_dict()
    return jsonify(dic_review), 200
