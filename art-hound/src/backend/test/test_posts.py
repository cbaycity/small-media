"""Tests for the posts functionality."""

from posts import createPost
import pytest
from typing import NamedTuple, Any, List
from test_login import TestUser
from login import newUser
from io import BytesIO
from werkzeug.datastructures import FileStorage


class ExamplePost(NamedTuple):
    username: str
    title: str
    description: str
    image: Any
    project: str = None


@pytest.mark.parametrize(
    "users,posts",
    [
        (
            [TestUser("test1", "test@gmail.com", "Password1")],
            [
                ExamplePost(
                    "test1",
                    "Sample Title",
                    "Sample Description",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                    "testUserProjectOne",
                ),
            ],
        ),
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            [
                ExamplePost(
                    "test1",
                    "Sample Title",
                    "Sample Description",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                    "testUserProjectOne",
                ),
            ],
        ),
    ],
)
def test_createPost(users: List[TestUser], posts: List[ExamplePost]):
    """Tests that create post successfully adds posts and images to the DB."""
    # Add users to the database.
    for user in users:
        newUser(user.username, user.email, user.password)

    # Add posts to the database.
    for post in posts:
        assert createPost(
            post.username, post.title, post.description, post.image, post.project
        )

    # List of file ids to assert are in FS later.
    file_ids = []

    # Assert that posts are in the DB.
    from backend_db import DB

    for post in posts:
        post_entry = DB["posts"].find_one({"title": post.title})
        assert post_entry["username"] == post.username
        # Check that the posts match up.
        file_ids.append(post_entry["image-id"])

    # Check that each image was added to the FS.
    from backend_db import FS

    for image in file_ids:
        image_entry = FS.get(image)
        assert image_entry.read() == b"Sample File"
        # Checks that the file was added correctly.


# Note: This file needs to test further functionality.
# 1. Test that projects are correctly linked to the post.
# 2. Test that a failure occurs if the linked project doesn't exist.
