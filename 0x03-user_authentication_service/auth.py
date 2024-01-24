#!/usr/bin/env python3
"""
4. Hash password
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
import logging


def _hash_password(password: str) -> bytes:
    """
    function that takes password and returns bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    function that generates uuid and returns a str
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        function that takes password and returns bytes
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        function that regsisters user
        args:
            emails: user email
            password: user password
        Returns:
            user object
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(
                    email=email, hashed_password=hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        function that validates credentials of a user
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user is not None:
                hashed_password = existing_user.hashed_password
                correct_password = bcrypt.checkpw(
                        password.encode('utf-8'), hashed_password)
                if correct_password:
                    return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        function that generates and saves session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            print(None)
