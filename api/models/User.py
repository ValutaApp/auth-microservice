from api.core import Mixin
from .base import db


class User(Mixin, db.Model):
    """User Table."""

    __tablename__ = "user"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)

    def __init__(self, name: str, email: str, password: str, isAdmin: bool ):
        self.name = name
        self.email = email
        self.password = password
        self.isAdmin = isAdmin

    def __repr__(self):
        return f"<User {self.email}>"
