"""Tests that the login functions work with MongoDB correctly."""

from login import newUser, login
from typing import List, NamedTuple
import pytest
from pymongo.database import Database


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
def test_new_user_login(users: List[TestUser], db: Database):
    """Tests that users are added to the database and that login works."""
    # Add Users
    for user in users:
        newUser(user.username, user.email, user.password, db)

    for user in users:
        assert login(user.username, user.password, db)


@pytest.mark.parametrize(
    "testname,users",
    [
        (
            "Duplicate Username",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test1", "test2@gmail.com", "Password2"),
            ],
        ),
        (
            "Duplicate Email",
            [
                TestUser("test1", "test@gmail.com", "Password1"),
                TestUser("test2", "test@gmail.com", "Password2"),
            ],
        ),
    ],
)
def test_new_user_fail(testname: str, users: List[TestUser], db: Database):
    """Tests that duplicate usernames and email can't be created."""
    print(testname)
    # Add the first user.
    newUser(users[0].username, users[0].email, users[0].password, db)
    # Check that the second user isn't added.

    assert newUser(users[1].username, users[1].email, users[1].password, db) == False
