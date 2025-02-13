"""Tests that the login functions work with MongoDB correctly."""

import datetime as dt
from typing import List, NamedTuple, Tuple

import pytest
from login import (addFriend, areFriends, checkUserAccess, getFriendRequests,
                   getUser, login, newUser, removeFriend, removeFriendRequest,
                   sendFriendRequest, userExists, validLogin)


class TestUser(NamedTuple):
    username: str
    email: str
    password: str


@pytest.mark.parametrize(
    "users",
    [
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
            ]
        )
    ],
)
def test_new_user_login(users: List[TestUser]):
    """Tests that users are added to the database and that login works."""
    # Add Users
    for user in users:
        newUser(user.username, user.email, user.password)

    for user in users:
        status, _ = login(user.username, user.password)
        assert status


@pytest.mark.parametrize(
    "testname,users,result",
    [
        (
            "Duplicate Username",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test1", "test2@gmail.com", "Password2"),
            ],
            (False, True),
        ),
        (
            "Duplicate Email",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test@gmail.com", "Password2"),
            ],
            (True, False),
        ),
        (
            "Duplicate Email and Username",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test1", "test@gmail.com", "Password2"),
            ],
            (False, False),
        ),
    ],
)
def test_new_user_fail(testname: str, users: List[TestUser], result: Tuple[bool, bool]):
    """Tests that duplicate usernames and email can't be created."""
    print(testname)
    # Add the first user.
    newUser(users[0].username, users[0].email, users[0].password)
    # Check that the second user isn't added.

    assert newUser(users[1].username, users[1].email, users[1].password) == result


@pytest.mark.parametrize(
    "users",
    [
        [
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test2", "test2@gmail.com", "Password2"),
            TestUser("test3", "test3@gmail.com", "Password!(#)"),
            TestUser("test3", "test3@gmail.com", "10hgTKLN900123##$%"),
        ]
    ],
)
def test_passwords_hashed(users: List[TestUser]):
    """Tests that the passwords are stored in a hashed form."""
    # Add the users to the database.

    for user in users:
        newUser(user.username, user.email, user.password)

    # Get the monkeypatched db.
    # Note: This cannot be done earlier because the db value changes for each test.
    from backend_db import DB

    # Check that the password isn't stored raw.
    for user in users:
        db_entry = DB["users"].find({"username": user.username})
        assert db_entry[0]["password"] != user.password


@pytest.mark.parametrize(
    "user, result, new_time",
    [
        (TestUser("test1", "test@gmail.com", "Password1"), True, dt.datetime.now()),
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            False,
            dt.datetime(year=1950, month=1, day=1),
        ),
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            False,
            dt.datetime.now() + dt.timedelta(days=-2),
        ),
    ],
)
def test_validLogin(user, result, new_time):
    """Tests that valid login works as expected."""
    # Create and Login user
    newUser(user.username, user.email, user.password)
    _, token = login(user.username, user.password)

    # Adjust time
    from backend_db import DB

    query = {"token": token}
    _ = DB["tokens"].update_one(query, {"$set": {"init-time": new_time}})

    # Check result
    assert validLogin(token) == result


@pytest.mark.parametrize(
    "users,use_email",
    [
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
                TestUser("test3", "test3@gmail.com", "Password3"),
            ],
            False,
        ),
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
                TestUser("test3", "test3@gmail.com", "Password3"),
            ],
            True,
        ),
    ],
)
def test_validLogin(users: List[TestUser], use_email: bool):
    """Tests that valid login works as expected."""
    # Create and Login user
    tokens = []
    for user in users:
        newUser(user.username, user.email, user.password)
        if not use_email:
            _, token = login(user.username, user.password)
        else:
            _, token = login(user.email, user.password)
        tokens.append(token)
    for user, token in zip(users, tokens):
        assert getUser(token)["username"] == user.username


@pytest.mark.parametrize(
    "user_one, user_two",
    [
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test2", "test2@gmail.com", "Password2"),
        )
    ],
)
def test_addFriend(user_one: TestUser, user_two: TestUser):
    """Checks that friends can be established correctly."""
    for user in [user_one, user_two]:
        newUser(user.username, user.email, user.password)

    # Add the friends.
    assert addFriend(user_one.username, user_two.username)

    # Assert that they're friends.
    from backend_db import DB

    first_user = DB["users"].find_one({"username": user_one.username})
    assert user_two.username in first_user["friends"]

    second_user = DB["users"].find_one({"username": user_two.username})
    assert user_one.username in second_user["friends"]


@pytest.mark.parametrize(
    "user_one, user_two",
    [
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test2", "test2@gmail.com", "Password2"),
        )
    ],
)
def test_removeFriend(user_one: TestUser, user_two: TestUser):
    """Tests that remove friend works as expected."""
    for user in [user_one, user_two]:
        newUser(user.username, user.email, user.password)

    # Add the friends.
    assert addFriend(user_one.username, user_two.username)
    assert removeFriend(user_one.username, user_two.username)

    # Assert that they're friends.
    from backend_db import DB

    first_user = DB["users"].find_one({"username": user_one.username})
    assert user_two.username not in first_user["friends"]

    second_user = DB["users"].find_one({"username": user_two.username})
    assert user_one.username not in second_user["friends"]


@pytest.mark.parametrize(
    "user_one, user_two",
    [
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test2", "test2@gmail.com", "Password2"),
        )
    ],
)
def test_removeFriendRequest(user_one: TestUser, user_two: TestUser):
    """Tests that remove friend request processes correctly."""
    for user in [user_one, user_two]:
        newUser(user.username, user.email, user.password)
    sendFriendRequest(user_one.username, user_two.username)
    from backend_db import DB

    second_user = DB["users"].find_one({"username": user_two.username})
    assert user_one.username in second_user["friend_requests"]

    removeFriendRequest(user_two.username, user_one.username)
    second_user = DB["users"].find_one({"username": user_two.username})
    assert user_one.username not in second_user["friend_requests"]


@pytest.mark.parametrize(
    "user_one, user_two",
    [
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test2", "test2@gmail.com", "Password2"),
        )
    ],
)
def test_addFriend_Fails(user_one, user_two):
    """Tests that addFriend fails when one of the users doesn't exist."""

    # Add the first user but assert that the function fails.
    newUser(user_one.username, user_one.email, user_one.password)

    assert addFriend(user_one.username, user_two.username) == False
    assert addFriend(user_two.username, user_one.username) == False


@pytest.mark.parametrize(
    "user_one, user_two",
    [
        (
            TestUser("test1", "test@gmail.com", "Password1"),
            TestUser("test2", "test2@gmail.com", "Password2"),
        )
    ],
)
def test_checkUserAccess(user_one, user_two):
    """Tests that addFriend fails when one of the users doesn't exist."""

    # Add the users
    newUser(user_one.username, user_one.email, user_one.password)
    newUser(user_two.username, user_two.email, user_two.password)

    # Assert that checkUserAccess fails when they aren't friends.
    assert checkUserAccess(user_one.username, user_two.username) == False

    # Asser that checkUserAccess passes for a user on itself.
    assert checkUserAccess(user_one.username, user_one.username)

    # Assert that checkUserAccess passes when they are friends.
    addFriend(user_one.username, user_two.username)
    assert checkUserAccess(user_one.username, user_two.username)


@pytest.mark.parametrize(
    "users,search_user,expectation",
    [
        (
            [TestUser("test1", "test@gmail.com", "Password1")],
            TestUser("test1", "test@gmail.com", "Password1"),
            True,
        ),
        (
            [TestUser("test1", "test@gmail.com", "Password1")],
            TestUser("test2", "test2@gmail.com", "Password2"),
            False,
        ),
    ],
)
def test_userExists(users: List[TestUser], search_user: TestUser, expectation: bool):
    """Tests that the user exists or doesn't correctly."""
    for user in users:
        newUser(user.username, user.email, user.password)
    if expectation:
        assert userExists(search_user.username) is not False
    else:
        assert userExists(search_user.username) is False


def test_areFriends():
    """Tests that the are friends returns correct values."""
    user_one = TestUser("test1", "test@gmail.com", "Password1")
    user_two = TestUser("test2", "test2@gmail.com", "Password2")
    for user in [user_one, user_two]:
        newUser(user.username, user.email, user.password)

    assert areFriends(user_one.username, user_two.username) == False

    addFriend(user_one.username, user_two.username)

    assert areFriends(user_one.username, user_two.username)


def test_sendFriendRequest():
    """Tests that the friend request is sent correctly."""
    user_one = TestUser("test1", "test@gmail.com", "Password1")
    user_two = TestUser("test2", "test2@gmail.com", "Password2")

    newUser(user_one.username, user_one.email, user_one.password)

    # Checks that sendFriendRequest fails when the second user doesn't exist.
    assert sendFriendRequest(user_one.username, user_two.username) == False

    newUser(user_two.username, user_two.email, user_two.password)

    # Checks that sendFriendRequest succeeds.
    assert sendFriendRequest(user_one.username, user_two.username)
    from login import USERS

    user_two_doc = USERS.find_one({"username": user_two.username})
    assert user_one.username in user_two_doc["friend_requests"]


def test_getFriendRequests():
    """Tests that get friend requests works well."""
    user_one = TestUser("test1", "test@gmail.com", "Password1")
    user_two = TestUser("test2", "test2@gmail.com", "Password2")
    for user in [user_one, user_two]:
        newUser(user.username, user.email, user.password)

    # Assert that user_one doesn't have any requests yet.
    assert getFriendRequests(user_one.username) == []
    assert sendFriendRequest(user_two.username, user_one.username)
    assert [user_two.username] == getFriendRequests(user_one.username)
