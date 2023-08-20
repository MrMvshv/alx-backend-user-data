#!/usr/bin/env python3
"""
auth functions here
"""
import bcrypt

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments
    returns bytes that is a salted hash of the input,
    hashed with bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            existing_user = None

        if existing_user:
            raise ValueError(f"User {email} already exists.")

        hashed_password = _hash_password(password)
        new_user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)

        return new_user
