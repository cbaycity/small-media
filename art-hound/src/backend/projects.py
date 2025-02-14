"""This module contains code for creating and processing projects."""

import datetime
import uuid
from typing import List

from werkzeug.datastructures import FileStorage

from backend_db import DB, FS

PROJECTS = DB["projects"]
"""Gets or creates a collection for projects."""

POSTS = DB["posts"]
USERS = DB["users"]


def _map_projects(project):
    """Maps a mongo db project doc to a dictionary."""
    result = {
        "title": (project["project_title"] if "project_title" in project else None),
        "username": project["username"] if "username" in project else None,
        "startDate": (project["startDate"] if "startDate" in project else None),
        "endDate": project["endDate"] if "endDate" in project else None,
        "description": (project["description"] if "description" in project else None),
        "image_id": (str(project["image_id"]) if "image_id" in project else None),
        "project_id": str(project["project_id"]),
    }
    return result


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
            "project_title": title,
        }
    )

    if len(user_projects.to_list()) > 0:
        return False  # A project with that same name for this user already exists.

    # Insert the image and get the image_id back.
    image_id = FS.put(image, filename=image.filename, content_type=image.content_type)

    PROJECTS.insert_one(
        {
            "project_id": str(uuid.uuid4()),
            "username": username,
            "project_title": title,
            "description": description,
            "image_id": image_id,
            "public": public,
            "startDate": startDate,
            "endDate": endDate,
        }
    )
    return True  # The project was added successfully.


def getUserProjects(username: str):
    """Returns a list of all of the project titles associated with a user."""
    projects = PROJECTS.find({"username": username}).to_list()
    return [_map_projects(project) for project in projects]


def getProjectPosts(username: str, title: str):
    """Returns a list of all of the project titles associated with a user."""
    project = PROJECTS.find_one({"username": username, "project_title": title})
    if project:
        project_id = str(project["project_id"])
    else:
        return [{"Error": "No Project with this title."}]
    posts = POSTS.find({"project_id": project_id}).sort("startDate", -1)
    return [
        {
            "title": post["title"],
            "username": post["username"],
            "startDate": post["startDate"].strftime("%Y-%m-%d"),
            "endDate": post["endDate"].strftime("%Y-%m-%d"),
            "description": post["description"],
            "image_id": str(post["image_id"]),
            "project": (post["related_project"] if post["project_id"] else None),
        }
        for post in posts
    ]


def projectAccessCheck(title: str, projectOwner: str, searchUser: str):
    """Returns the username of a project owner."""
    project = PROJECTS.find_one({"project_title": title, "username": projectOwner})
    if not project:
        return False

    owner_user = USERS.find_one({"username": project["username"]})
    if not owner_user:
        return False
    if (
        owner_user["public"]
        or searchUser in owner_user["friends"]
        or searchUser == owner_user["username"]
    ):
        return True
    return False


def getProject(username: str, project_id: str):
    """Returns basic information on a project."""
    project = PROJECTS.find_one({"project_id": project_id, "username": username})
    if not project:
        return False
    else:
        # Remove not needed attributes and return the project.
        project.pop("_id")
        # Ensure that only strings, which are jsonify-able, are returned.
        project["project_id"] = str(project["project_id"])
        project["image_id"] = str(project["image_id"])
        return project


def getFriendProjects(friends: List[str]):
    """Returns a list of all of the project titles associated with friends of a user."""
    result = []
    for username in friends:
        projects = PROJECTS.find({"username": username}).to_list()
        for project in projects:
            result.append(_map_projects(project))
    return result
