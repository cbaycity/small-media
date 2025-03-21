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
    response = website.get(
        f"/find_user/{search_user.username}",
        content_type="application/json",
        data=json.dumps(
            {
                "token": token,
            }
        ),
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


def test_processFriendRequest(website):
    """Tests that the processFriendRequest can add and remove friends."""
    user = TestUser("test1", "test@gmail.com", "Password1")
    friend = TestUser("test2", "test2@gmail.com", "Password2")

    newUser(user.username, user.email, user.password)
    newUser(friend.username, friend.email, friend.password)
    valid_user, token = login(user.username, user.password)
    assert valid_user

    assert sendFriendRequest(friend.username, user.username)

    # Ensures that the friends are added.
    response = website.get(
        f"/process_friend_request",
        content_type="application/json",
        data=json.dumps(
            {
                "token": token,
                "target_user": friend.username,
                "add_or_remove": "add",
            }
        ),
    )
    assert response.status_code == 200
    from backend_db import DB

    user_doc = DB["users"].find_one({"username": user.username})
    assert friend.username in user_doc["friends"]
    # Tests that the friend was added.

    assert friend.username not in user_doc["friend_requests"]
    # Tests that the friend request was removed.

    # Tests removing a friend.
    response = website.get(
        f"/process_friend_request",
        content_type="application/json",
        data=json.dumps(
            {
                "token": token,
                "target_user": friend.username,
                "add_or_remove": "remove",
            }
        ),
    )
    assert response.status_code == 200
    user_doc = DB["users"].find_one({"username": user.username})
    assert friend.username not in user_doc["friends"]


# Add Tests for PhotoFiles

# Add tests for getUserPosts

# Add tests for AccountCreation

# Add tests for userLogin

# Add tests for ValidLogin

# Add tests for ProcessPost

# Add tests for ProcessProject

# Add tests for UserProjects

# Add tests for ProjectPage
