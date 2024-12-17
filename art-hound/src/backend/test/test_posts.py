"""Tests for the posts functionality."""

from posts import createPost, singleUserFeed, multiUserFeed
import pytest
from typing import NamedTuple, Any, List, Union, Tuple
from test_login import TestUser
from login import newUser
from io import BytesIO
from werkzeug.datastructures import FileStorage
from datetime import datetime
from login import addFriend


class ExamplePost(NamedTuple):
    username: str
    title: str
    description: str
    image: Any
    project: str = None
    startDate: str = "2024-01-01"
    endDate: str = "2024-01-01"
    public: bool = False


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
                    None,
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
                    None,
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
            post.username,
            post.title,
            post.description,
            post.startDate,
            post.endDate,
            post.image,
            post.project,
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


@pytest.mark.parametrize(
    "test_name,users,friends,posts,test_user,query_user,expectation",
    [
        (
            "One user querying another",
            [
                TestUser("test", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            [("test", "test2")],
            [
                ExamplePost(
                    "test",
                    "Sample Title",
                    "Sample Description",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            "test2",
            "test",
            [
                {
                    "title": "Sample Title",
                    "username": "test",
                    "startDate": datetime.strptime("2024-01-01", "%Y-%m-%d"),
                    "endDate": datetime.strptime("2024-01-01", "%Y-%m-%d"),
                    "description": "Sample Description",
                }
            ],
        ),
        (
            "One user querying themselves",
            [
                TestUser("test", "test@gmail.com", "Password1"),
            ],
            [],
            [
                ExamplePost(
                    "test",
                    "Sample Title",
                    "Sample Description",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
                ExamplePost(
                    "test",
                    "Sample Title2",
                    "Sample Description2",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            "test",
            "test",
            [
                {
                    "title": "Sample Title",
                    "username": "test",
                    "startDate": datetime.strptime("2024-01-01", "%Y-%m-%d"),
                    "endDate": datetime.strptime("2024-01-01", "%Y-%m-%d"),
                    "description": "Sample Description",
                },
                {
                    "title": "Sample Title2",
                    "username": "test",
                    "startDate": datetime.strptime("2024-01-01", "%Y-%m-%d"),
                    "endDate": datetime.strptime("2024-01-01", "%Y-%m-%d"),
                    "description": "Sample Description2",
                },
            ],
        ),
    ],
)
def test_singleUserFeed(
    test_name: str,
    users: List[TestUser],
    friends: List[Tuple[str, str]],
    posts: List[ExamplePost],
    test_user: TestUser,
    query_user: TestUser,
    expectation: Union[List[ExamplePost], bool],
):
    """Tests that singleUserFeed returns posts as expected."""
    print(test_name)  # Prints use case name for debugging.

    # Add users to the database.
    for user in users:
        newUser(user.username, user.email, user.password)

    # Ensures users are friends.
    for user, add_friend in friends:
        addFriend(user, add_friend)

    # Add posts to the database.
    for post in posts:
        assert createPost(
            post.username,
            post.title,
            post.description,
            post.startDate,
            post.endDate,
            post.image,
            post.project,
        )

    result = singleUserFeed(test_user, query_user)
    image_id_found = []
    for result_dict in result:
        image_id_found.append(result_dict.pop("image-id"))
    assert result == expectation

    from backend_db import FS

    all_images = FS.find({}).to_list()
    all_image_ids = [doc._id for doc in all_images]
    for id in image_id_found:
        assert id in all_image_ids


@pytest.mark.parametrize(
    "test_name,users,posts,test_user,query_user",
    [
        (
            "One user querying another",
            [
                TestUser("test", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            [
                ExamplePost(
                    "test",
                    "Sample Title",
                    "Sample Description",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            "test2",
            "test",
        ),
    ],
)
def test_singleUserFeed_noAuth(
    test_name: str,
    users: List[TestUser],
    posts: List[ExamplePost],
    test_user: TestUser,
    query_user: TestUser,
):
    """Tests that singleUserFeed fails when the first user isn't
    authorized to see the second user's content."""

    print(f"Test: {test_name}")

    # Add users to the database.
    for user in users:
        newUser(user.username, user.email, user.password)

    # Add posts to the database.
    for post in posts:
        assert createPost(
            post.username,
            post.title,
            post.description,
            post.startDate,
            post.endDate,
            post.image,
            post.project,
        )
    assert False == singleUserFeed(test_user, query_user)
