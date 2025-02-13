"""Tests that the functions in Backend DB process requests as expected."""

import datetime as datetime
from io import BytesIO
from typing import List

import pytest
from backend_db import getPhotoUser
from login import newUser
from posts import createPost
from projects import createProject
from test_login import TestUser
from test_posts import ExamplePost
from test_projects import ExampleProject
from werkzeug.datastructures import FileStorage


@pytest.mark.parametrize(
    "user,project,post",
    [
        (
            TestUser("test1", "test@gmail.com", "Password1"),
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
            ExamplePost(
                "test1",
                "Sample Title",
                "Sample Description",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
                None,
            ),
        ),
    ],
)
def test_getPhotoUser(user: TestUser, project: ExampleProject, post: ExamplePost):
    """Tests that createProject successfully adds projects to the DB."""
    # Add users to the database.
    assert newUser(user.username, user.email, user.password)

    # Add project to the database.
    assert createProject(
        project.username, project.title, project.description, project.image
    )

    assert createPost(
        post.username,
        post.title,
        post.description,
        post.startDate,
        post.endDate,
        post.image,
    )

    from backend_db import DB

    # Assert that the project username is found correctly.
    project_entry = DB["projects"].find_one({"project_title": project.title})
    assert getPhotoUser(project_entry["image_id"]) == project.username

    # Assert that post username is found correctly.
    post_entry = DB["posts"].find_one({"title": post.title})
    assert getPhotoUser(post_entry["image_id"]) == post.username
