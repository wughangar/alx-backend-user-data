#!/usr/bin/env python3
"""
3. Auth class
"""

from flask import request


class Auth:
    """ auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ 
        public method

