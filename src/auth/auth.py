import hashlib

from src.app.app import app
from src.data.models import User


def hash_password(password: str):
    return hashlib.sha256(str.encode(password)).hexdigest()


def register(username: str, password: str):
    User(
        username=username,
        password=hash_password(password)
    )


def authenticate(username: str, password: str):
    user = User.get_or_none(username=username)
    if user is not None and user.password == hash_password(password):
        app.sessions.add_session(username)
