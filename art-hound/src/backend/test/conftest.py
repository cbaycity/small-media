"""This creates some necessary resources for testing features.

The main resource needed is a mongodb client.
"""

import gridfs
import pytest
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
"""A client using local host, encapsulates tests in the Python env."""
# Note: Don't switch this to call the normal database. DON'T DELETE PROD.


@pytest.fixture(autouse=True)
def set_test_db(monkeypatch):
    """Sets up a mongodb database for each test."""
    # Note: This automatically applies to each test.
    test_db = client.test_database
    test_fs = gridfs.GridFS(test_db)
    monkeypatch.setattr("backend_db.DB", test_db)
    monkeypatch.setattr("backend_db.FS", test_fs)
    monkeypatch.setattr("login.USERS", test_db["users"])
    monkeypatch.setattr("posts.USERS", test_db["users"])
    monkeypatch.setattr("posts.POSTS", test_db["posts"])
    monkeypatch.setattr("projects.PROJECTS", test_db["projects"])
    monkeypatch.setattr("projects.POSTS", test_db["posts"])
    monkeypatch.setattr("posts.PROJECTS", test_db["projects"])
    monkeypatch.setattr("image_query.USERS", test_db["users"])
    monkeypatch.setattr("image_query.POSTS", test_db["posts"])
    monkeypatch.setattr("image_query.PROJECTS", test_db["projects"])
    monkeypatch.setattr("posts.FS", test_fs)
    monkeypatch.setattr("projects.FS", test_fs)
    monkeypatch.setattr("image_query.FS", test_fs)
    # Need to reset manually each module that imports DB because each test needs a new import.
    yield test_db, test_fs
    for collection in test_db.list_collection_names():
        test_db[collection].delete_many({})  # Remove all records from the database.
