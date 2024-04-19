from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.modules.auth.dependencies import AuthServiceDep
from src.modules.auth.exceptions.exceptions import InvalidAuthDataError
from src.modules.auth.views.schemas import TokenGet

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post(path='/create_token',
                  status_code=201,
                  response_model=TokenGet,
                  name='Create an access token')
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       auth_service: AuthServiceDep) -> dict[str, str]:
    try:
        return await auth_service.create_token(form_data=form_data)
    except InvalidAuthDataError as exc:
        raise HTTPException(status_code=409, detail=f'{exc}')
