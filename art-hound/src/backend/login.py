"""This is a module to track if users have an account with ArtHound."""

import datetime
import secrets
from functools import lru_cache
from typing import Tuple

from werkzeug.security import check_password_hash, generate_password_hash

from backend_db import DB

# Get or create a collection of usernames and passwords.
USERS = DB["users"]

TOKEN_LENGTH = 32  # URL Safe length for tokens.


def login(username: str, password: str) -> bool:
    """Checks if a username and password exist and the user can login.

    args:
        username: The user's username.
        password: The user's unhashed password.
    """
    # NOTE: need to return a cookie in the future.
    user = USERS.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        userToken = secrets.token_urlsafe(TOKEN_LENGTH)
        DB["tokens"].insert_one(
            {
                "token": userToken,
                "username": user["username"],
                "init-time": datetime.datetime.now(),
            }
        )
        return True, userToken
    return False, ""


def newUser(username: str, email: str, password: str) -> Tuple[bool, bool]:
    """Creates a new user iff the username doesn't exist and the email doesn't exist.

    args:
        username: The user's username.
        email: The user's email address.
        password: The user's unhashed password.

    Returns:
        username_new: True if the provided username was uniquely new.
        email_new: True if the provided email was uniquely new.
    """
    query = {"$or": [{"username": username}, {"email": email}]}
    user = USERS.find_one(query)

    if not user:
        newUser = {
            "username": username,
            "password": generate_password_hash(password),
            "email": email,
            "friends": [],
            "public": False,
        }
        USERS.insert_one(newUser)
        return True, True
    return (user["username"] != username, user["email"] != email)


def validLogin(token: str):
    """Checks if a login token is valid."""
    db_entry = DB["tokens"].find_one({"token": token})
    if db_entry and db_entry[
        "init-time"
    ] > datetime.datetime.now() + datetime.timedelta(days=-1):
        return True
    return False


@lru_cache(maxsize=16384)
def getUser(token: str):
    """Returns the username related to a token unless the token is invalid."""
    db_entry = DB["tokens"].find_one({"token": token})
    if db_entry and db_entry[
        "init-time"
    ] > datetime.datetime.now() + datetime.timedelta(days=-1):
        return db_entry["username"]
    return False


def addFriend(first_user: str, second_user: str):
    """Friendship."""
    # Check that user and new_friend exist.
    first_user_doc = USERS.find_one({"username": first_user})
    second_user_doc = USERS.find_one({"username": second_user})
    if not (first_user_doc and second_user_doc):
        return False

    # Add friends to docs.
    USERS.update_one(
        {"username": first_user},
        {"$addToSet": {"friends": second_user}},
    )
    USERS.update_one(
        {"username": second_user},
        {"$addToSet": {"friends": first_user}},
    )
    return True
