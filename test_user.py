"""Doc."""

from .user import User


def test1():
    """Doc."""
    user1 = User('id')
    user2 = User('id')
    assert user1 == user2
