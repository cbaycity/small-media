"""This module sets up the backend DB."""

import os

import gridfs
from pymongo import MongoClient
from bson import ObjectId


# MongoDB Connection.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
CLIENT = MongoClient(MONGO_URI)
DB = CLIENT.production  # monkey patch switch to client.testdatabase for tests.


# Set up the image store.
FS = gridfs.GridFS(DB)


def photoProcess(image_id: str):
    """Returns an image from the FS assuming that authentication has occured."""
    return FS.get(ObjectId(image_id))
