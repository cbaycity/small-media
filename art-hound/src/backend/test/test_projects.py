"""Tests that ensure that projects are successfully added and managed."""

from io import BytesIO
from typing import Any, Dict, List, NamedTuple, Tuple

import pytest
from test_login import TestUser
from test_posts import ExamplePost
from werkzeug.datastructures import FileStorage

from login import addFriend, newUser
from posts import createPost
from projects import (createProject, getProjectPosts, getUserProjects,
                      projectAccessCheck)


class ExampleProject(NamedTuple):
    username: str
    title: str
    description: str
    image: Any
    public: bool = False


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


@pytest.mark.parametrize(
    "name,users,init_projects,test_case",
    [
        (
            "Failure with matching project title and user.",
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
        ),
        (
            "Failure with null title.",
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
            ExampleProject(
                "test1",
                None,
                "Sample Description",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
            ),
        ),
        (
            "Failure with title that has no characters.",
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
            ExampleProject(
                "test1",
                "",
                "Sample Description",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
            ),
        ),
    ],
)
def test_createProjectFailures(
    name: str,
    users: List[TestUser],
    init_projects: List[ExampleProject],
    test_case: ExampleProject,
):
    """Tests that createProject fails when needed."""
    # Fail without a title or with a matching title for the user.

    print(f"Test: {name}")

    # Add users to the database.
    for user in users:
        newUser(user.username, user.email, user.password)

    # Add posts to the database.
    for project in init_projects:
        assert createProject(
            project.username, project.title, project.description, project.image
        )

    assert (
        createProject(
            test_case.username, test_case.title, test_case.description, test_case.image
        )
        is False
    )


@pytest.mark.parametrize(
    "users, projects, expectedProjectNames",
    [
        (
            [TestUser("test1", "test@gmail.com", "Password1")],
            [
                ExampleProject(
                    "test1",
                    "sample one",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                )
            ],
            ["sample one"],
        ),
        (
            [TestUser("test1", "test@gmail.com", "Password1")],
            [
                ExampleProject(
                    "test1",
                    "sample one",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
                ExampleProject(
                    "test1",
                    "sample two",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            ["sample one", "sample two"],
        ),
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            [
                ExampleProject(
                    "test1",
                    "sample one",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
                ExampleProject(
                    "test1",
                    "sample two",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            ["sample one", "sample two"],
        ),
    ],
)
def test_getUserProjects(
    users: List[TestUser],
    projects: List[ExampleProject],
    expectedProjectNames: List[str],
):
    """Checks that after adding projects each project is returned by expectedProjectNames"""
    for user in users:
        newUser(user.username, user.email, user.password)

    for project in projects:
        assert createProject(
            project.username, project.title, project.description, project.image
        )

    result = getUserProjects(users[0].username)

    # Checks that each project returned has the required fields.
    for project in result:
        for field in [
            "title",
            "username",
            "startDate",
            "endDate",
            "description",
            "image-id",
        ]:
            assert field in project

    project_names = set([project["title"] for project in result])

    # Checks that the first user has all of thier projects.
    for name in expectedProjectNames:
        assert name in project_names


@pytest.mark.parametrize(
    "users,project,posts,expected_posts",
    [
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            ExampleProject(
                "test1",
                "sample one",
                "test case",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
            ),
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
                    "sample one",
                ),
            ],
            [
                {
                    "title": "Sample Title",
                    "username": "test1",
                    "startDate": "2024-01-01",
                }
            ],
        )
    ],
)
def test_getProjectPosts(
    users: List[TestUser],
    project: List[ExampleProject],
    posts: List[ExamplePost],
    expected_posts: List[Dict[str, Any]],
):
    """Tests that a created project can have it's posts collected."""
    for user in users:
        newUser(user.username, user.email, user.password)

    assert createProject(
        project.username, project.title, project.description, project.image
    )

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

    # Check the end dict of posts.
    result = getProjectPosts(project.title)

    from backend_db import DB

    all_posts = DB["posts"].find({})
    for post in all_posts:
        print(post)

    # Check that the same number of posts is correct.
    assert len(result) == len(expected_posts)

    # Check that the right elements are there.
    for result, expected in zip(result, expected_posts):
        for key, val in expected.items():
            assert result[key] == val


@pytest.mark.parametrize(
    "users,projects,searchProject,test_user,friends,expected_result",
    [
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
            ],
            [
                ExampleProject(
                    "test1",
                    "sample one",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            ExampleProject(
                "test1",
                "sample one",
                "test case",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
            ),
            TestUser("test1", "test@gmail.com", "Password1"),
            None,
            True,
        ),
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
            ],
            [
                ExampleProject(
                    "test1",
                    "sample one",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            ExampleProject(
                "test1",
                "Not Found",
                "test case",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
            ),
            TestUser("test1", "test@gmail.com", "Password1"),
            None,
            False,
        ),
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
            ],
            [
                ExampleProject(
                    "test1",
                    "sample one",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            ExampleProject(
                "test1",
                "sample one",
                "test case",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
            ),
            TestUser("test2", "test@gmail.com", "Password1"),
            None,
            False,
        ),
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ],
            [
                ExampleProject(
                    "test1",
                    "sample one",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
                ExampleProject(
                    "test2",
                    "sample two",
                    "test case",
                    FileStorage(
                        stream=BytesIO(b"Sample File"),
                        filename="testFile",
                        content_type="test/plain",
                    ),
                ),
            ],
            ExampleProject(
                "test1",
                "sample one",
                "test case",
                FileStorage(
                    stream=BytesIO(b"Sample File"),
                    filename="testFile",
                    content_type="test/plain",
                ),
            ),
            TestUser("test2", "test2@gmail.com", "Password2"),
            ("test1", "test2"),
            True,
        ),
    ],
)
def test_getProjectOwner(
    users: List[TestUser],
    projects: List[ExampleProject],
    searchProject: ExampleProject,
    test_user: TestUser,
    friends: Tuple[str, str],
    expected_result: str,
):
    """Tests that get project owner works as expected."""
    for user in users:
        newUser(user.username, user.email, user.password)

    for project in projects:
        assert createProject(
            project.username, project.title, project.description, project.image
        )

    if friends:
        addFriend(friends[0], friends[1])

    assert (
        projectAccessCheck(
            searchProject.title, searchProject.username, test_user.username
        )
        == expected_result
    )
