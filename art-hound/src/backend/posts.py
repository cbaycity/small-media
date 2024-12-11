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
