"""This module contains code to create posts and add them to the database."""

import uuid
from datetime import datetime

from werkzeug.datastructures import FileStorage

from backend_db import DB, FS

# Get or create a collection for Posts.
POSTS = DB["posts"]
USERS = DB["users"]
PROJECTS = DB["projects"]


def createPost(
    username: str,
    title: str,
    description: str,
    startDate: str,
    endDate: str,
    image: FileStorage,
    project: str = None,
    public: bool = False,
):
    """Adds a post to the user's database and looks up related projects if needed."""
    if project is not None:
        related_project = PROJECTS.find_one(
            {
                "username": username,
                "project": "project-title",
            }
        )["project_id"]
    else:
        related_project = None

    # Insert the image and get the image-id back.
    image_id = FS.put(image, filename=image.filename, content_type=image.content_type)

    POSTS.insert_one(
        {
            "post_id": str(uuid.uuid4()),
            "username": username,
            "title": title,
            "description": description,
            "startDate": datetime.strptime(startDate, "%Y-%m-%d"),
            "endDate": datetime.strptime(endDate, "%Y-%m-%d"),
            "image-id": image_id,
            "project-id": related_project,
            "public": public,
        }
    )
    return True  # The post was added successfully.


def singleUserFeed(user: str, queryUsername: str):
    """Gets the feed for a single user."""
    if not (isinstance(user, str) or isinstance(queryUsername, str)):
        raise TypeError(
            f"Need to provide strings to this function. User: {user}, queryUsername:{queryUsername}"
        )

    if user != queryUsername:
        # Need to ensure the users are friends or the account is public.
        user_doc = USERS.find_one({"username": user})
        if not (user_doc["public"] or queryUsername in user_doc["friends"]):
            return False

    query = {
        "username": queryUsername,
    }
    data = POSTS.find(query).sort("startDate", -1)
    return [
        {
            "title": post["title"],
            "username": post["username"],
            "startDate": post["startDate"],
            "endDate": post["endDate"],
            "description": post["description"],
            "image-id": str(post["image-id"]),
        }
        for post in data
    ]


def multiUserFeed(username: str):
    """Gets the feed for friends of a user."""
    friends = USERS.find_one({})
    # NOTE: Needs to return the same data structure as singleUserFeed so that the front end can easily process things.
    return "NEED TO PROCESS FRIENDS BEFORE BUILDING THIS FEED TYPE."


# Plan for managing access to images.
# When the user requests a feed, they get back post info.
# In that post info, the original user will be included.
# So the query then sends a request to get the image.
# This request has a token and the original user.
# So query the users table to check that the image is from that user
# Check that the two users are friends.

# This is efficient because querying the token is fast
# and query the user's table by user can be quick.
# The last query to the file service for the image should be fast.
# Note: when processing friends,
# you need to ensure that each user document includes the full friends list.

# Should start with the process for a user to query for their own images.
