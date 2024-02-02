from datetime import datetime
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field

from src.user.userenums import UserStatus


class UserDB(Document):
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[str, Indexed(unique=True)]
    password: str
    join_date: datetime = Field(default_factory=datetime.utcnow)
    status: UserStatus = Field(default=UserStatus.default)
