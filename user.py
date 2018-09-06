"""Doc."""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    """Doc."""

    def __init__(self, id):
        """Doc."""
        self.id = id
        self.password_hash = None
        self.auth = False

    def set_password(self, password):
        """Doc."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Doc."""
        self.auth = check_password_hash(self.password_hash, password)
        return self.auth

    # @property
    # def is_authenticated(self):
    #     """Doc."""
    #     return self.auth
