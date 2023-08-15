#!/usr/bin/env python3
"""
session authentication system class
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id

        Args:
            user_id (str, optional): Defaults to None.

        Returns (str):
            None if user_id is None
            None if user_id is not a string
            SessionID
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        ssid = uuid4()
        str_ssid = str(ssid)

        self.user_id_by_session_id[str_ssid] = user_id

        return str_ssid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID

        Args:
            session_id (str, optional): Defaults to None.

        Returns (str):
            None if session_id is None
            None if session_id is not a string
            value (the User ID) for the key session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """(overload) returns a User instance based on a cookie value

        Args:
            request: Defaults to None.
        Returns:
            User
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ deletes the user session / logout

        Args:
            request: Defaults to None.
        """

        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_cookie]
        return True
