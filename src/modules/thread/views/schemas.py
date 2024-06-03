from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints

from src.core.presentation.schemas import FromAttrsBaseModel, GUIDMixin


class _CommentBase(FromAttrsBaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=250)]


class CommentCreate(_CommentBase):
    pass


class CommentGet(_CommentBase, GUIDMixin):
    created_at: datetime


class _ThreadBase(FromAttrsBaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)]
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=500)]


class ThreadCreate(_ThreadBase):
    pass


class ThreadGet(_ThreadBase, GUIDMixin):
    is_active: bool
    created_at: datetime


class ThreadWithCommentsGet(ThreadGet):
    comments: list[CommentGet]
