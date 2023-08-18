#!/usr/bin/env python3
"""
auth functions here
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments
    returns bytes that is a salted hash of the input,
    hashed with bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
