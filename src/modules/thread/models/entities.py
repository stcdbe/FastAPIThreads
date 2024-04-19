from dataclasses import dataclass, field
from datetime import datetime

from src.core.models.base import AbstractEntity


@dataclass
class Comment(AbstractEntity):
    text: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Thread(AbstractEntity):
    title: str
    text: str
    is_active: bool = field(default=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    comments: list[Comment] = field(default_factory=list)
