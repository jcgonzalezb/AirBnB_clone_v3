#!/usr/bin/python3
"""
View for Users that handles all RESTful API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """ Retrieves a list of all State object"""
    users_all = []
    users = storage.all("User").values()
    for user in users:
        users_all.append(user.to_dict())

    return jsonify(users_all)


@app_views.route('/users/<user_id>',  methods=['GET'], strict_slashes=False)
def user_get(user_id):
    """ Handles GET method """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """Deletes a user"""
    users = storage.get("User", user_id)
    if users is None:
        abort(404)
    else:
        storage.delete(users)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    elif 'email' not in data:
        abort(400, "Missing email")
    elif 'password' not in data:
        abort(400, "Missing password")
    else:
        new_user = User(**data)
        storage.new(new_user)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_put(user_id):
    """ Updates a User. Handles PUT method """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)

    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key in data.keys():
        if key in ignore_keys:
            pass
        else:
            setattr(obj, key, data[key])
    storage.save()
    res = obj.to_dict()
    return jsonify(res), 200
