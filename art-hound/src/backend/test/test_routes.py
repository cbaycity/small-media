"""This file contains all of the tests for each route in main.py."""

import pytest
from test_login import TestUser
from login import newUser, login
import json


def test_public(website):
    """Tests that public files are always returned."""
    response = website.get("/public/feed.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["Content-Type"]
    assert ".feed-body" in response.text


# Add Tests for PhotoFiles

# Add tests for getUserPosts

# Add tests for AccountCreation

# Add tests for userLogin

# Add tests for ValidLogin

# Add tests for ProcessPost

# Add tests for ProcessProject

# Add tests for UserProjects

# Add tests for ProjectPage


@pytest.mark.parametrize(
    "user, search_user, expectation",
    [
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test1", "test@gmail.com", "Password1"),
            True,
        ),
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test2", "test2@gmail.com", "Password2"),
            False,
        ),
    ],
)
def test_friendSearch(
    website, user: TestUser, search_user: TestUser, expectation: bool
):
    """Ensures that friendSearch functionality works as expected."""
    newUser(user.username, user.email, user.password)
    _, token = login(user.username, user.password)
    response = website.get(
        f"/find_user/{search_user.username}",
        content_type="application/json",
        data=json.dumps({"token": token}),
    )
    data = json.loads(response.data.decode("utf-8"))
    data["UserExists"] == expectation
