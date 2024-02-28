from datetime import datetime

from beanie import Document
from pydantic import Field

from src.thread.thread_schemas import CommentGet


class ThreadDB(Document):
    title: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    comments: list[CommentGet] = Field(default_factory=list)
