"""Tests that ensure that projects are successfully added and managed."""

from projects import createProject
import pytest
from typing import NamedTuple, Any, List
from test_login import TestUser
from login import newUser
from io import BytesIO
from werkzeug.datastructures import FileStorage


class ExampleProject(NamedTuple):
    username: str
    title: str
    description: str
    image: Any


@pytest.mark.parametrize(
    "users,projects",
    [
        (
            [TestUser("test1", "test@gmail.com", "Password1")],
            [
                ExampleProject(
                    "test1",
                    "Sample Title",
                    "Sample Description",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
        ),
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            [
                ExampleProject(
                    "test1",
                    "Sample Title",
                    "Sample Description",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
        ),
    ],
)
def test_createProject(users: List[TestUser], projects: List[ExampleProject]):
    """Tests that createProject successfully adds projects to the DB."""
    # Add users to the database.
    for user in users:
        newUser(user.username, user.email, user.password)

    # Add posts to the database.
    for project in projects:
        assert createProject(
            project.username, project.title, project.description, project.image
        )

    # List of file ids to assert are in FS later.
    file_ids = []

    # Assert that posts are in the DB.
    from backend_db import DB

    for project in projects:
        project_entry = DB["projects"].find_one({"project-title": project.title})
        assert project_entry["username"] == project.username
        # Check that the posts match up.
        file_ids.append(project_entry["image-id"])

    # Check that each image was added to the FS.
    from backend_db import FS

    for image in file_ids:
        image_entry = FS.get(image)
        assert image_entry.read() == b"Sample File"
        # Checks that the file was added correctly.
