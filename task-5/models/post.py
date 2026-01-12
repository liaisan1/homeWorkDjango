
from dataclasses import dataclass, field
from enum import Enum

from abstracts.base import BaseModel
from abstracts.meta import Meta


class PostStatus(Enum):
    """Post status enum."""

    CREATED = 0
    PUBLISHED = 1
    DELETED = 2



@dataclass(repr=False, kw_only=True)
class Post(BaseModel, metaclass=Meta):
    """Post model class.

    Args:
        title (Optional[str]): Post title
        description (Optional[str]): Post summary
        text (Optional[str]): Post main text
        status(PostStatus): User status
    """

    title: str | None = None
    description: str | None = None
    text: str | None = None
    status: PostStatus = field(default=PostStatus.CREATED)
