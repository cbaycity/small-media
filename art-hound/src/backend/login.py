"""This is a module to track if users have an account with ArtHound."""

from pymongo import MongoClient
from pymongo.database import Database
import os
from typing import Tuple, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB Connection.
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client.production  # monkey patch switch to client.testdatabase for tests.

# Create a collection of usernames and passwords.
collection_list = db.list_collection_names()
if "users" not in collection_list:
    USERS = db.create_collection("users")


def login(username: str, password: str) -> bool:
    """Checks if a username and password exist and the user can login.

    args:
        username: The user's username.
        password: The user's unhashed password.
    """
    # NOTE: need to return a cookie in the future.
    user = db["users"].find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        return True  # Return a cookie for the session. Create a session.
    return False


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
    user = db["users"].find_one(query)

    if not user:
        newUser = {
            "username": username,
            "password": generate_password_hash(password),
            "email": email,
        }
        db["users"].insert_one(newUser)
        return True, True
    return (user["username"] != username, user["email"] != email)
