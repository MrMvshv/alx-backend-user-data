#!/usr/bin/env python3
"""
auth class for all authentication system
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """
    authentication methods here
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns false
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request will be the Flask request object
        """
        return None
