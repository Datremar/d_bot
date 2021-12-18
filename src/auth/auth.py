import hashlib

from src.data.models import User


def register(username: str, password: str):
    hash = hashlib.sha256(str.encode(password)).hexdigest()

    User(
        username=username,
        password=hash
    )


def authenticate(username: str, password: str):
    pass
