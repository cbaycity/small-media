"""Tests that the login functions work with MongoDB correctly."""

import datetime as dt
from typing import List, NamedTuple, Tuple

import pytest
from login import addFriend, getUser, login, newUser, validLogin


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
    "users",
    [
        (
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test2@gmail.com", "Password2"),
                TestUser("test3", "test3@gmail.com", "Password3"),
            ]
        ),
    ],
)
def test_validLogin(users):
    """Tests that valid login works as expected."""
    # Create and Login user
    tokens = []
    for user in users:
        newUser(user.username, user.email, user.password)
        _, token = login(user.username, user.password)
        tokens.append(token)
    for user, token in zip(users, tokens):
        assert getUser(token) == user.username


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

    for user in DB["users"].find({}):
        print(f"All users: {user}")

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
def test_addFriend_Fails(user_one, user_two):
    """Tests that addFriend fails when one of the users doesn't exist."""

    # Add the first user but assert that the function fails.
    newUser(user_one.username, user_one.email, user_one.password)

    assert addFriend(user_one.username, user_two.username) == False
    assert addFriend(user_two.username, user_one.username) == False
