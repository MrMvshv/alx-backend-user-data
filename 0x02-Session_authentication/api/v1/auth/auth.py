#!/usr/bin/env python3
"""
auth class for all authentication system
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    authentication methods here
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if path is None
        Returns True if excluded_paths is None or empty
        Returns True if path is not in excluded_paths
        Returns False if path in excluded_paths
        slash tolerant
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Handling slash tolerance by ensuring the paths end with '/'
        path = path.rstrip('/') + '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        returns None - request will be the Flask request object
        """
        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            return None

        return authorization_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request

        Args:
            request : Defaults to None.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')

        return request.cookies.get(session_name)
