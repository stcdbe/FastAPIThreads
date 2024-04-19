from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints, EmailStr, UUID4

from src.core.presentation.schemas import AttrsBaseModel
from src.modules.user.models.enums import UserStatus


class _UserBase(AttrsBaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=50,
                                               pattern=r'^[a-z0-9_-]*$')]
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=50)]


class UserCreate(_UserBase):
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=6,
                                               max_length=72)]


class UserPatch(UserCreate):
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=50,
                                               pattern=r'^[a-z0-9_-]*$')] | None = None
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=50)] | None = None
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=6,
                                               max_length=72)] | None = None


class UserGet(_UserBase):
    guid: UUID4
    join_date: datetime
    status: UserStatus
