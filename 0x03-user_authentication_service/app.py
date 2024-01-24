#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth
import logging


logging.disable(logging.WARNING)


AUTH = Auth()

app = Flask(__name__)


@app.route("/")
def welcome():
    """ function returns jsonified string"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def register_user():
    """ function that registers the user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = AUTH.register_user(email, password)
        return jsonify(
                {"email": new_user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    function that allows log in
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)

    session = AUTH.create_session(email)
    feedback = jsonify({"email": email, "message": "logged in"})
    feedback.set_cookie("session_id", session_id)
    return feedback


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    session_id = request.cookies.get('session_id')
    existing_user = AUTH.get_user_from_session_id(session_id)

    if existing_user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
