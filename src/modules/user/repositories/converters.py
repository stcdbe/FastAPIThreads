from collections.abc import Mapping
from typing import Any

from src.modules.user.models.entities import User


def convert_user_doc_to_entity(data: Mapping[str, Any]) -> User:
    return User(
        guid=data["guid"],
        username=data["username"],
        email=data["email"],
        password=data["password"],
        join_date=data["join_date"],
        status=data["status"],
    )
