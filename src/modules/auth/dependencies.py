from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.modules.auth.exceptions.exceptions import InvalidAuthDataError
from src.modules.auth.services.services import AuthService
from src.modules.user.models.entities import User
from src.modules.user.models.enums import UserStatus

TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='api/v1/auth/create_token'))]
AuthServiceDep = Annotated[AuthService, Depends()]


async def get_current_user(auth_service: AuthServiceDep, token: TokenDep) -> User:
    try:
        return await auth_service.validate_token(token=token)
    except InvalidAuthDataError as exc:
        raise HTTPException(status_code=401, detail=f'{exc}')


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def check_current_user_is_admin(user: CurrentUserDep) -> User:
    if user.status != UserStatus.admin:
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return user


CurrentUserAdminDep = Annotated[User, Depends(check_current_user_is_admin)]
