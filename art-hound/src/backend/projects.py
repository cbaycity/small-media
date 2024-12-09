"""This module contains code for creating and processing projects."""

from backend_db import DB, FS
import uuid
from werkzeug.datastructures import FileStorage

PROJECTS = DB["projects"]
"""Gets or creates a collection for projects."""


def createProject(username: str, title: str, description: str, image: FileStorage):
    """Adds a post to the user's database and looks up related projects if needed."""

    # Assert that the user doesn't have a project
    user_projects = PROJECTS.find(
        {
            "username": username,
            "project-title": title,
        }
    )

    if len(user_projects.to_list()) > 0:
        return False  # A project with that same name for this user already exists.

    # Insert the image and get the image-id back.
    image_id = FS.put(image, filename=image.filename, content_type=image.content_type)

    PROJECTS.insert_one(
        {
            "project_id": str(uuid.uuid4()),
            "username": username,
            "project-title": title,
            "description": description,
            "image-id": image_id,
        }
    )
    return True  # The project was added successfully.
