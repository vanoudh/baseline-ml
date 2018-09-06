"""Doc."""

from .user import User


def test1():
    """Doc."""
    user1 = User('id', 'password')
    user2 = User('id', 'password')
    assert user1 == user2
