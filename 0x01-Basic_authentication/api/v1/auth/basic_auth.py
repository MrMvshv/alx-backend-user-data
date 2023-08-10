#!/usr/bin/env python3
"""
basic authentication system class
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """
    Basic authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Returns the base64 part of the authheader
        Args:
            authorization_header (str)
        Returns:
                 None or Base64 part of header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        b64_string = authorization_header.split(' ')[-1]

        return b64_string

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string
        Args:
             base64_authorization_header (str)
        Returns:
              str: None or decoded value
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(decode)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value.
        Args:
            decoded_base64_authorization_header (str)
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':')

        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns User based on email and password
        Args:
            user_email: str, user_pwd: str
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User
        """
        auth_header = self.authorization_header(request)

        if auth_header is not None:
            b64 = self.extract_base64_authorization_header(auth_header)
            if b64 is not None:
                decoded = self.decode_base64_authorization_header(b64)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)
        return
