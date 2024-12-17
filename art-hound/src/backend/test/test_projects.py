"""Tests that ensure that projects are successfully added and managed."""

from io import BytesIO
from typing import Any, List, NamedTuple

import pytest
from test_login import TestUser
from werkzeug.datastructures import FileStorage

from login import newUser
from projects import createProject, getUserProjects


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
    # Always check the projects of the first user.
    for name in expectedProjectNames:
        assert name in result
