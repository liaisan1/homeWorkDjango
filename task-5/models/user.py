
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from abstracts.base import BaseModel
from abstracts.meta import Meta


class UserStatus(Enum):
    """User status enum."""

    CREATED = 0
    CONFIRMED = 1
    BANNED = 2



@dataclass(repr=False, kw_only=True)
class User(BaseModel, metaclass=Meta):
    """User model class.

    Args:
        username (Optional[str]): User login
        password (Optional[str]): User password
        status(UserStatus): User status
    """

    username: str | None = None
    password: str | None = None
    status: UserStatus = field(default=UserStatus.CREATED)

