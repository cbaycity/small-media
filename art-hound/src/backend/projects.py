"""This module contains code for creating and processing projects."""

import uuid

from werkzeug.datastructures import FileStorage

from backend_db import DB, FS

import datetime

PROJECTS = DB["projects"]
"""Gets or creates a collection for projects."""


def createProject(
    username: str,
    title: str,
    description: str,
    image: FileStorage,
    public: bool = False,
    startDate=datetime.datetime.now(),
    endDate=None,
):
    """Adds a post to the user's database and looks up related projects if needed."""

    if title is None or len(title) == 0:
        return False

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
            "public": public,
            "startDate": startDate,
            "endDate": endDate,
        }
    )
    return True  # The project was added successfully.


def getUserProjects(username: str):
    """Returns a list of all of the project titles associated with a user."""
    projects = PROJECTS.find({"username": username}).to_list()
    return [
        {
            "title": project["project-title"] if "project-title" in project else None,
            "username": project["username"] if "username" in project else None,
            "startDate": project["startDate"] if "startDate" in project else None,
            "endDate": project["endDate"] if "endDate" in project else None,
            "description": project["description"] if "description" in project else None,
            "image-id": str(project["image-id"]) if "image-id" in project else None,
        }
        for project in projects
    ]
