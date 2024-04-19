from dataclasses import dataclass, field
from datetime import datetime

from src.core.models.base import AbstractEntity
from src.modules.user.models.enums import UserStatus


@dataclass
class User(AbstractEntity):
    username: str
    email: str
    password: str
    join_date: datetime = field(default_factory=datetime.utcnow)
    status: UserStatus = field(default=UserStatus.default)
