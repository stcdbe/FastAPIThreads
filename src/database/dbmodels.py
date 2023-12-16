from typing import Annotated
from datetime import datetime

from beanie import Document, Indexed, Link
from pydantic import Field

from src.thread.threadschemas import CommentGet


class UserDB(Document):
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[str, Indexed(unique=True)]
    password: str
    join_date: datetime = Field(default_factory=datetime.utcnow)


class ThreadDB(Document):
    title: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    comments: list[CommentGet] = Field(default_factory=list)
    creator: Link['UserDB']
