"""This is a module to track if users have an account with ArtHound."""

from typing import Dict, NamedTuple, Set


class Account(NamedTuple):
    username: str
    email: str
    password: str


USERS: Dict[str, Account] = {}
"""A mapping of users to their passwords."""
EMAILS: Set[str] = set()

# NOTE: Need to query a database with users and not store them in a dictionary.


def login(username, password) -> bool:
    """Checks if a username and password exist and the user can login."""
    # NOTE: need to return a cookie in the future.
    if username in USERS:
        if password == USERS[username].password:
            return True
    return False


def newUser(username, password, email) -> bool:
    """If a username doesn't exist, the email doesn't exist, and the password is correct create a new user."""
    if username not in USERS and email not in EMAILS:
        newUser = Account(username, email, password)
        USERS[username] = newUser
        EMAILS.add(email)
        return True
    return False
