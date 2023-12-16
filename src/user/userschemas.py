from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, EmailStr
from beanie import PydanticObjectId



class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=50)]
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=50)]


class UserCreate(User):
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=6,####################
                                               max_length=72)]


class UserPatch(UserCreate):
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=50)] | None = None
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=50)] | None = None
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=6,##########################
                                               max_length=72)] | None = None


class UserGet(User):
    id: PydanticObjectId
    join_date: datetime
