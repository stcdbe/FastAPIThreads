from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, StringConstraints, ConfigDict


class CommentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: Annotated[str, StringConstraints(strip_whitespace=True,
                                           min_length=5,
                                           max_length=250)]


class CommentGet(CommentCreate):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ThreadCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Annotated[str, StringConstraints(strip_whitespace=True,
                                            min_length=5,
                                            max_length=100)]
    text: Annotated[str, StringConstraints(strip_whitespace=True,
                                           min_length=5,
                                           max_length=500)]


class ThreadGet(ThreadCreate):
    id: PydanticObjectId
    is_active: bool
    created_at: datetime


class ThreadWithCommentsGet(ThreadGet):
    comments: list[CommentGet]
