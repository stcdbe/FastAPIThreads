from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import DecodeError, InvalidTokenError, decode, encode

from src.config import settings
from src.modules.auth.exceptions.exceptions import InvalidAuthDataError
from src.modules.auth.utils.hasher.base import AbstractHasher
from src.modules.auth.utils.hasher.bcrypt import BcryptHasher
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository
from src.modules.user.repositories.mongo import MongoUserRepository


class AuthService:
    _repository: AbstractUserRepository
    _hasher: AbstractHasher

    def __init__(
        self,
        repository: Annotated[AbstractUserRepository, Depends(MongoUserRepository)],
        hasher: Annotated[AbstractHasher, Depends(BcryptHasher)],
    ) -> None:
        self._repository = repository
        self._hasher = hasher

    def _generate_token(self, sub: str, exp_delta: timedelta) -> str:
        expires = datetime.utcnow() + exp_delta
        to_encode = {"exp": expires, "sub": sub}
        return encode(
            payload=to_encode,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    async def create_token(self, form_data: OAuth2PasswordRequestForm) -> dict[str, str]:
        user = await self._repository.get_one(username=form_data.username)
        exc = InvalidAuthDataError("Incorrect username or password")

        if not user:
            raise exc

        if not self._hasher.verify_psw(psw_to_check=form_data.password, hashed_psw=user.password):
            raise exc

        token = self._generate_token(sub=str(user.guid), exp_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES))
        return {"access_token": token, "token_type": "bearer"}

    async def validate_token(self, token: str) -> User:
        exc = InvalidAuthDataError("Could not validate credentials")

        try:
            payload = decode(
                jwt=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            guid = UUID(payload["sub"])
        except (InvalidTokenError, DecodeError, KeyError, ValueError) as e:
            raise exc from e

        user = await self._repository.get_one(guid=guid)

        if not user:
            raise exc

        return user
