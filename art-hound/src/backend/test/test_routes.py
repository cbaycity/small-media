"""This file contains all of the tests for each route in main.py."""

import json

import pytest
from test_login import TestUser

from login import addFriend, login, newUser, sendFriendRequest, userExists


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
def test_searchFriends(
    website, user: TestUser, search_user: TestUser, expectation: bool
):
    """Ensures that friendSearch functionality works as expected."""
    newUser(user.username, user.email, user.password)
    valid_user, token = login(user.username, user.password)
    assert valid_user
    website.set_cookie("auth_token", token)
    response = website.get(
        f"/find_user/{search_user.username}",
        content_type="application/json",
    )
    data = json.loads(response.data.decode("utf-8"))
    data["UserExists"] == expectation


def test_returnFriendRequests(website):
    """Tests that returnFriendRequests returns a list of friends."""
    user = TestUser("test1", "test@gmail.com", "Password1")
    friend = TestUser("test2", "test2@gmail.com", "Password2")

    newUser(user.username, user.email, user.password)
    newUser(friend.username, friend.email, friend.password)
    valid_user, token = login(user.username, user.password)
    assert valid_user
    website.set_cookie("auth_token", token)
    response = website.get(
        f"/friend_requests",
        content_type="application/json",
    )
    assert response.data.decode("utf-8") == str([]) + "\n"
    assert sendFriendRequest(friend.username, user.username)
    next_response = website.get(
        f"/friend_requests",
        content_type="application/json",
    )
    assert (
        next_response.data.decode("utf-8")
        == str([f"{friend.username}"]).replace("'", '"') + "\n"
    )


def test_returnFriendList(website):
    """Tests that returnFriendRequests returns a list of friends."""
    user = TestUser("test1", "test@gmail.com", "Password1")
    friend = TestUser("test2", "test2@gmail.com", "Password2")

    newUser(user.username, user.email, user.password)
    newUser(friend.username, friend.email, friend.password)
    valid_user, token = login(user.username, user.password)
    assert valid_user
    website.set_cookie("auth_token", token)
    response = website.get(
        f"/friendlist",
        content_type="application/json",
    )
    assert response.data.decode("utf-8") == str([]) + "\n"
    assert addFriend(friend.username, user.username)
    next_response = website.get(
        f"/friendlist",
        content_type="application/json",
    )
    assert (
        next_response.data.decode("utf-8")
        == str([f"{friend.username}"]).replace("'", '"') + "\n"
    )
