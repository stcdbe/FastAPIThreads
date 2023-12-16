from datetime import timedelta
from typing import Annotated, Any

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.config import settings
from src.auth.authschemas import Token
from src.user.userservice import get_user_by_username_db
from src.auth.authutils import generate_token
from src.auth.hasher import Hasher


login_router = APIRouter()


@login_router.post('/create_token',
                   status_code=201,
                   response_model=Token,
                   name='Create an access token')
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Any:
    user = await get_user_by_username_db(username=form_data.username)

    if not user:
        raise HTTPException(status_code=404, detail='Not found')

    if not Hasher.verify_psw(psw=form_data.password, hashed_psw=user.password):
        raise HTTPException(status_code=400, detail='Invalid username or password')

    token = await generate_token(user_id=str(user.id),
                                 expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES))
    return {'access_token': token, 'token_type': 'bearer'}
