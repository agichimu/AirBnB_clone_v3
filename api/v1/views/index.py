#!/usr/bin/python3
"""returns status of server"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """returns jsonified status"""
    return jsonify({"status": "OK"})
