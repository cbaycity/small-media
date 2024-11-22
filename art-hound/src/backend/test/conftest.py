"""This creates some necessary resources for testing features.

The main resource needed is a mongodb client.
"""

from pymongo import MongoClient
import pytest
import os

client = MongoClient("mongodb://localhost:27017/")
"""A client using local host, encapsulates tests in the Python env."""
# Note: Don't switch this to call the normal database. DON'T DELETE PROD.


@pytest.fixture
def db():
    """Sets up a mongodb database for each test."""
    # Note: This automatically applies to each test with a db arguement.
    test_db = client.test_database
    yield test_db  # Return the database to be used in testing.
    for collection in test_db.list_collection_names():
        test_db[collection].delete_many({})  # Remove all records from the database.
