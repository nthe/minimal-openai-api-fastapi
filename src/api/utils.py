from time import time
from uuid import uuid4


def get_hash() -> str:
    """Generate a random hash."""
    return uuid4().hex


def get_time() -> int:
    """Get the current time."""
    return int(time())
