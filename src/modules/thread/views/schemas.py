from datetime import datetime
from typing import Annotated

from pydantic import UUID4, StringConstraints

from src.core.presentation.schemas import AttrsBaseModel


class _CommentBase(AttrsBaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=250)]


class CommentCreate(_CommentBase):
    pass


class CommentGet(_CommentBase):
    guid: UUID4
    created_at: datetime


class _ThreadBase(AttrsBaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)]
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=500)]


class ThreadCreate(_ThreadBase):
    pass


class ThreadGet(_ThreadBase):
    guid: UUID4
    is_active: bool
    created_at: datetime


class ThreadWithCommentsGet(ThreadGet):
    comments: list[CommentGet]
