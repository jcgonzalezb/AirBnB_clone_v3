#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from api.v1.views import app_views

from models import storage
from flask import jsonify


classes = ["Amenity", "City", "Place", "Review", "State", "User"]


@app_views.route('/status')
def status():
    """ Returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_stats():
    """ Create an endpoint that retrieves the number of each objects by type"""
    count_dic = {}
    for cls in classes:
        count_dic[cls] = storage.count(cls)

    return jsonify(count_dic)
