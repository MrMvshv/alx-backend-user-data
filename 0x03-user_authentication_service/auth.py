#!/usr/bin/env python3
"""
auth functions here
"""
import bcrypt
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
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


def _generate_uuid() -> str:
    """ Generate uuid
        Return:
            uuid in string
    """
    UUID = uuid4()

    return str(UUID)


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user in system
        """
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

    def valid_login(self, email: str, password: str) -> bool:
        """ Verify is there a valid login
            Args:
                email: email of the user
                password: string hashed
            Return:
                True If its valid information
        """
        if email is None or password is None:
            return False

        try:
            user: User = self._db.find_user_by(email=email)
            passwd: bytes = str.encode(user.hashed_password)
            valid: bool = bcrypt.checkpw(password.encode('utf-8'),
                                         passwd)

            return valid
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Make session id and update in the database
            Args:
                email: email of the user
            Return:
                session id
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user((user.id), session_id=sess_id)

            return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """ Find a user based in session id
            Args:
                session_id: Session identificator
            Return:
                User otherwise None
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)

            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: str) -> None:
        """ Destroy session
            Args:
                user_id: Destroy the session id
            Return:
                None
        """
        try:
            self._db.update_user(user_id, session_id=None)

            return None
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generate reset password token
            Args:
                email: To reset the password token
            Return:
                token generated
        """
        if email is None:
            raise ValueError

        try:
            user = self._db.find_user_by(email=email)

            token: str = _generate_uuid()
            self._db.update_user((user.id), reset_token=token)

            return token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update Password
            Args:
                email: To reset the password token
            Return:
                token generat ed
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except (NoResultFound, InvalidRequestError):
            raise ValueError

        new_passwd = _hash_password(password)

        self._db.update_user(
            (user.id), hashed_password=new_passwd,
            reset_token=None)

        return None
