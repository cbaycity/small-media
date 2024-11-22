"""This is a module to track if users have an account with ArtHound."""

from pymongo import MongoClient
from pymongo.database import Database
import os

# MongoDB Connection.
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client.mydatabase

# Create a collection of usernames and passwords.
collection_list = db.list_collection_names()
if "users" not in collection_list:
    USERS = db.create_collection("users")


def login(username: str, password: str, db: Database = db) -> bool:
    """Checks if a username and password exist and the user can login.

    args:
        username: The user's username.
        password: The user's unhashed password.
        db: The mongo database to call from. Using a non-default should be used only for testing.
    """
    # NOTE: need to return a cookie in the future.
    user = db["users"].find_one({"username": username})
    if user and user["password"] == password:
        return True
    return False


def newUser(username: str, email: str, password: str, db: Database = db) -> bool:
    """Creates a new user iff the username doesn't exist and the email doesn't exist.

    args:
        username: The user's username.
        email: The user's email address.
        password: The user's unhashed password.
        db: The mongo database to call from. Using a non-default should be used only for testing.
    """
    query = {"$or": [{"username": username}, {"email": email}]}

    if not db["users"].find_one(query):
        newUser = {"username": username, "password": password, "email": email}
        db["users"].insert_one(newUser)
        return True
    return False
