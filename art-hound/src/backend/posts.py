"""This module contains code to create posts and add them to the database."""

from backend_db import DB, FS
import uuid
from werkzeug.datastructures import FileStorage

# Get or create a collection for Posts.
POSTS = DB["posts"]


def createPost(
    username: str, title: str, description: str, image: FileStorage, project: str = None
):
    """Adds a post to the user's database and looks up related projects if needed."""
    if project is not None:
        related_project = None  # Temp None, need to lookup related project.

    # Insert the image and get the image-id back.
    image_id = FS.put(image, filename=image.filename, content_type=image.content_type)

    POSTS.insert_one(
        {
            "post_id": str(uuid.uuid4()),
            "username": username,
            "title": title,
            "description": description,
            "image-id": image_id,
            "project-id": related_project,
        }
    )
    return True  # The post was added successfully.


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
