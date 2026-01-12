from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    DELETED = "deleted"


@dataclass
class User:
    user_id: int
    username: str
    email: str
    status: UserStatus = field(default=UserStatus.ACTIVE)

    def __str__(self):
        return f"ID: {self.user_id}, Имя: {self.username}, Email: {self.email}, Статус: {self.status.value}"

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            user_id=data["user_id"],
            username=data["username"],
            email=data["email"],
            status=UserStatus(data["status"])
        )