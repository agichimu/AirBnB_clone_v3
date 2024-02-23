#!/usr/bin/python3
"""api module concearned with cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route("/places", methods=['GET'])
def get_places():
    """Retrieves the list of all Place objects"""
    all_users = storage.all('Place')
    values = [val.to_dict() for val in all_users.values()]
    return jsonify(values)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """retrieves a place object"""
    value = storage.get('Place', place_id)
    return jsonify(value.to_dict()) if value is not None else abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """deletes a place"""
    value = storage.get('Place', place_id)
    abort(404) if value is None else value.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places", methods=['POST'])
def post_place():
    """posts data to existing json blob"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    if 'name' not in blob:
        return jsonify({"error: Missing name"}), 400
    """create it using the blob data"""
    newObject = Place(**blob)
    """save it to persist in memory"""
    newObject.save()
    return jsonify(newObject.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """updates a Place object"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    """the state_id is not in database"""
    val = storage.get('Place', place_id)
    if val is None:
        abort(404)
    """because our api deals __class__,id, name, created_at,updated_at and we are to
    Ignore keys: id, created_at and updated_at"""
    val['name'] = blob['name']
    """to persist in storage"""
    val.save()
    return jsonify(val.to_dict())
