#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
