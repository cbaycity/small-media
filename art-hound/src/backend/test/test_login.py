"""Tests that the login functions work with MongoDB correctly."""

from login import newUser, login
from typing import List, NamedTuple, Tuple
import pytest


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
    from login import db

    # Check that the password isn't stored raw.
    for user in users:
        db_entry = db["users"].find({"username": user.username})
        assert db_entry[0]["password"] != user.password
