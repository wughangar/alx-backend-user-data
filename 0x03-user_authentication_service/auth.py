#!/usr/bin/env python3
"""
4. Hash password
"""

import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    function that takes password and returns bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        function that regsisters user
        args:
            emails: user email
            password: user password
        Returns:
            user object
        """
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists.")
        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
        return new_user
