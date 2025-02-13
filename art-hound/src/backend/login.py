"""This is a module to track if users have an account with ArtHound."""

import datetime
import secrets
from typing import Any, Dict, Tuple, Union

from backend_db import DB
from werkzeug.security import check_password_hash, generate_password_hash

# Get or create a collection of usernames and passwords.
USERS = DB["users"]

TOKEN_LENGTH = 32  # URL Safe length for tokens.


def login(username: str, password: str) -> bool:
    """Checks if a username and password exist and the user can login.

    args:
        username: The user's username.
        password: The user's unhashed password.
    """
    user = USERS.find_one({"username": username})
    if not user:
        user = USERS.find_one({"email": username})
    if user and check_password_hash(user["password"], password):
        userToken = secrets.token_urlsafe(TOKEN_LENGTH)
        DB["tokens"].insert_one(
            {
                "token": userToken,
                "username": user["username"],
                "init-time": datetime.datetime.now(),
            }
        )
        return user["username"], userToken
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


def getUser(token: str) -> Union[bool, Dict[Any, Any]]:
    """Returns the token's related user record as a dict unless the token is invalid."""
    db_entry = DB["tokens"].find_one({"token": token})
    if db_entry and db_entry[
        "init-time"
    ] > datetime.datetime.now() + datetime.timedelta(days=-1):
        user_doc = USERS.find_one({"username": db_entry["username"]})
        return dict(user_doc) if user_doc else False
    return False


def addFriend(first_user: str, second_user: str):
    """Friendship."""
    # Check that user and new_friend exist.
    first_user_doc = USERS.find_one({"username": first_user})
    second_user_doc = USERS.find_one({"username": second_user})
    if not (first_user_doc and second_user_doc) or first_user == second_user:
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


def removeFriend(first_user: str, second_user: str):
    """Removes a friend between the two users."""
    # Check that user and new_friend exist.
    first_user_doc = USERS.find_one({"username": first_user})
    second_user_doc = USERS.find_one({"username": second_user})
    if not (first_user_doc and second_user_doc) or first_user == second_user:
        return False

    # Add friends to docs.
    USERS.update_one(
        {"username": first_user},
        {"$pullAll": {"friends": [second_user]}},
    )
    USERS.update_one(
        {"username": second_user},
        {"$pullAll": {"friends": [first_user]}},
    )
    return True


def areFriends(first_user: str, second_user: str):
    """Checks if two users are friends."""
    first_user_doc = USERS.find_one({"username": first_user})
    if second_user in first_user_doc["friends"]:
        return True
    return False


def sendFriendRequest(first_user: str, second_user: str) -> bool:
    """Sends a friend request from the first user to the second user.

    Returns True if successfully sent a request and false otherwise.
    """
    # Check that the second user exists.
    second_user_doc = USERS.find_one({"username": second_user})

    if not second_user_doc:
        return False

    update = USERS.update_one(
        {"_id": second_user_doc["_id"]}, {"$addToSet": {"friend_requests": first_user}}
    )
    return True if update.modified_count == 1 else False


def getFriendRequests(username: str):
    """Returns the usernames of people that have sent friend requests."""
    user_doc = USERS.find_one({"username": username})
    if not user_doc or "friend_requests" not in user_doc:
        return []
    else:
        return user_doc["friend_requests"]


def removeFriendRequest(username: str, target_request: str):
    """Removes a user's request to friend another."""
    USERS.update_one(
        {"username": username}, {"$pullAll": {"friend_requests": [target_request]}}
    )


def checkUserAccess(first_user: str, second_user: str):
    """Returns True if two users are friends and false otherwise."""
    if first_user == second_user:
        return True
    first_friends = USERS.find_one({"username": first_user})["friends"]
    if second_user not in first_friends:
        return False
    second_friends = USERS.find_one({"username": second_user})["friends"]
    if first_user not in second_friends:
        return False
    return True


def userExists(username: str):
    """Returns True if the user exists."""
    user = USERS.find_one({"username": username})
    if user:
        return dict(user)
    return False
