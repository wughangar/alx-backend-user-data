#!/usr/bin/env python3
"""
6. Basic auth
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar, List
from models.user import User
from flask import Flask, Request


class BasicAuth(Auth):
    """
    class that inherts from Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        method that returns base64 part of authorization header
        for a basic authentication
        """
        if authorization_header is None or not \
           isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic'):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        function that returns the decoded value of a bae64 str
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_bytes.decode('utf-8')
            return decoded_value
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        function that returns user eail and password from base64 decoded
        """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_password = decoded_base64_authorization_header.split(
                ':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        function that returns the user instance based on his email
        and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search(user_email)
        if not user_list:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a given request
        """
        if request is None or not isinstance(request, Request):
            return None

        authorization_header = request.headers.get('Authorization')

        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                authorization_header)

        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)

        if decoded_auth_header is None:
            return None

        user_email, user_password = self.extract_user_credentials(
                decoded_auth_header)

        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
