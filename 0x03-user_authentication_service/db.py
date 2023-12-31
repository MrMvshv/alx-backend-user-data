#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): User's email
            hashed_password (str): Hashed password

        Returns:
            User: The created User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
            self._session.refresh(new_user)
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by filtering with the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The found User object.

        Raises:
            NoResultFound: If no results are found.
            InvalidRequestError: If wrong query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound("No user found.")

            return user
        except InvalidRequestError as error:
            self._session.rollback()
            raise error

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        locate user to update,
        update user’s attributes as passed in the args
        commit changes to database.
        If argument that does not correspond to a user attribute,
        raise a ValueError.
        """
        user = self.find_user_by(id=user_id)

        if not user:
            raise ValueError("User not found")

        allowed_attributes = {
            "email", "hashed_password", "session_id", "reset_token"
        }

        for attr, value in kwargs.items():
            if attr in allowed_attributes:
                setattr(user, attr, value)
            else:
                raise ValueError(f"Invalid user attribute: {attr}")

        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()
