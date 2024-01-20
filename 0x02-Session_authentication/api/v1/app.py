#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


auth_typ = getenv("AUTH_TYPE")
if auth_typ == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()

public_paths = ['/api/v1/status', '/api/v1/unauthorized',
                '/api/v1/forbidden', '/api/v1/users']


@app.before_request
def before_request():
    """
    before request handler
    """
    print("DEBUG: Request Path:", request.path)
    print("DEBUG: Is Public Path?", request.path in public_paths)
    if auth and request.path not in public_paths:
        if not auth.require_auth(request.path, public_paths):
            print("DEBUG: Authentication required but not enforced")
            abort(401)
        if not auth.authorization_header(request):
            print("DEBUG: Authorization header missing")
            abort(401)
        if not auth.current_user(request):
            print("DEBUG: No current user identified")
            abort(403)

    request.current_user = auth.current_user(request)
    print("DEBUG: Current User:", request.current_user)

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized error handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden error handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
