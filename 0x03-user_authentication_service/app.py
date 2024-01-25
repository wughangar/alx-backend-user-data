#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    function that handles get profile request
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    """
    function that generates reset token for resetting users password
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
