#!/usr/bin/env python3
"""
3. Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        public method
        Returns:
            True if path is None or excluded_paths is None or empty.
            False if path is in excluded_paths (slash tolerant).
        """
        if path is None or not excluded_paths:
            return True
        else:
            return path.rstrip('/') in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        public authorization method
        Returns:
            The Authorization header value otherwise.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        public method
        """
        return None
