#!/usr/bin/python3
"""api module concearned with cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_reviews(place_id):
    """Retrieves the list of all reviews in a place object"""
    all_places = storage.get('Place', place_id)
    values = [val.to_dict() for val in all_places.reviews]
    return jsonify(values)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """retrieves a review object"""
    value = storage.get('Review', review_id)
    return jsonify(value.to_dict()) if value is not None else abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """deletes a review"""
    value = storage.get('Review', review_id)
    abort(404) if value is None else value.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def post_review(place_id):
    """posts data to existing json blob"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    if 'name' not in blob:
        return jsonify({"error: Missing name"}), 400
    """create it using the blob data"""
    newObject = Review(**blob)
    """save it to persist in memory"""
    newObject['place_id'] = place_id
    newObject.save()
    return jsonify(newObject.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """updates a Review object"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    """the state_id is not in database"""
    val = storage.get('Review', review_id)
    if val is None:
        abort(404)
    """because our api deals __class__,id, name, created_at,updated_at and we are to
    Ignore keys: id, created_at and updated_at"""
    val['name'] = blob['name']
    """to persist in storage"""
    val.save()
    return jsonify(val.to_dict())
