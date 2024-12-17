"""Tests that check the internal logic of image processing functions."""

from image_query import process_image
import pytest
from login import newUser, addFriend
from io import BytesIO
from werkzeug.datastructures import FileStorage
from login import addFriend
from typing import List, Tuple
from test_login import TestUser
from test_posts import ExamplePost
from test_projects import ExampleProject
from posts import createPost
from projects import createProject


@pytest.mark.parametrize(
    "test_name,users,post,friends,username",
    [
        (
            "Can view post between friends.",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
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
            [("test1", "test2")],
            "test2",
        ),
        (
            "Can view public post.",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
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
                public=True,
            ),
            [],
            "test2",
        ),
    ],
)
def test_process_image_posts(
    test_name: str,
    users: List[TestUser],
    post: ExamplePost,
    friends: List[Tuple[str, str]],
    username: str,
):
    """Tests that process_image gets images from posts."""
    # Prints test_name for debugging
    print(test_name)

    for user in users:
        newUser(user.username, user.email, user.password)

    # Add posts to the database.
    assert createPost(
        post.username,
        post.title,
        post.description,
        post.startDate,
        post.endDate,
        post.image,
        post.project,
        post.public,
    )

    # Assert that posts are in the DB.
    from backend_db import DB

    image_id = DB["posts"].find_one(
        {
            "username": post.username,
            "title": post.title,
            "description": post.description,
        }
    )["image-id"]

    # Create friends if needed.
    for pair in friends:
        addFriend(pair[0], pair[1])

    # Image-Found
    result = process_image(username, image_id)
    assert result == b"Sample File"


@pytest.mark.parametrize(
    "test_name,users,project,friends,username",
    [
        (
            "Can view a project between friends.",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
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
            [("test1", "test2")],
            "test2",
        ),
        (
            "Can view a public project.",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            ExampleProject(
                "test1",
                "Sample Title",
                "Sample Description",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
                public=True,
            ),
            [],
            "test2",
        ),
    ],
)
def test_process_image_projects(
    test_name: str,
    users: List[TestUser],
    project: ExampleProject,
    friends: List[Tuple[str, str]],
    username: str,
):
    """Tests that process_image gets images from projects."""
    print(f"Test: {test_name}")

    for user in users:
        newUser(user.username, user.email, user.password)

    # Assert that posts are in the DB.
    from backend_db import DB

    assert createProject(
        project.username,
        project.title,
        project.description,
        project.image,
        project.public,
    )

    # Create friends if needed.
    for pair in friends:
        addFriend(pair[0], pair[1])

    image_id = DB["projects"].find_one(
        {
            "username": project.username,
            "project-title": project.title,
            "description": project.description,
        }
    )["image-id"]

    # Image-Found
    result = process_image(username, image_id)
    assert result == b"Sample File"


@pytest.mark.parametrize(
    "test_name,users,post,project,username",
    [
        (
            "Cannot view private post without friends.",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
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
            None,
            "test2",
        ),
        (
            "Cannot view private project without friends.",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            None,
            ExampleProject(
                "test1",
                "Sample Title",
                "Sample Description",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
                public=False,
            ),
            "test2",
        ),
    ],
)
def test_process_image_unauthorized(
    test_name: str,
    users: List[TestUser],
    post: ExamplePost,
    project: ExampleProject,
    username: str,
):
    """Tests that process_image gets images cannot get unauthorized images."""

    print(f"Test: {test_name}")

    for user in users:
        newUser(user.username, user.email, user.password)

    # Assert that posts are in the DB.
    from backend_db import DB

    # Add posts to the database.
    if post:
        assert createPost(
            post.username,
            post.title,
            post.description,
            post.startDate,
            post.endDate,
            post.image,
            post.project,
            post.public,
        )
        image_id = DB["posts"].find_one(
            {
                "username": post.username,
                "title": post.title,
                "description": post.description,
            }
        )["image-id"]
        assert process_image(username, image_id) == "Not authorized to view this image."

    if project:
        assert createProject(
            project.username,
            project.title,
            project.description,
            project.image,
            project.public,
        )

        image_id = DB["projects"].find_one(
            {
                "username": project.username,
                "project-title": project.title,
                "description": project.description,
            }
        )["image-id"]
        assert process_image(username, image_id) == "Not authorized to view this image."


def test_process_image_not_found():
    """Tests that process_image gets images from projects."""
    # Nothing inserted into the DB, this should always fail.
    assert process_image("test", "fake-image-id") == "Image not found."
