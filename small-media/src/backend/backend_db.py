"""This module sets up the backend DB."""

import os

import gridfs
from bson import ObjectId
from pymongo import MongoClient

# MongoDB Connection.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
CLIENT = MongoClient(MONGO_URI)
DB = CLIENT.production  # monkey patch switch to client.testdatabase for tests.


# Set up the image store.
FS = gridfs.GridFS(DB)


def photoProcess(image_id: str):
    """Returns an image from the FS assuming that authentication has occured."""
    return FS.get(ObjectId(image_id))


def getPhotoUser(image_id: str):
    """Returns the user associated with a specific photo.

    Checks for the photo in the posts and projects collections.
    """
    post = DB["posts"].find_one({"image_id": ObjectId(image_id)})
    project = DB["projects"].find_one({"image_id": ObjectId(image_id)})
    document = post if post else project
    return document["username"]
