
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus
from src.auth.schemas import Token, CreateUserModel
from .utils import authenticate_user, create_access_token, get_current_user
from datetime import timedelta
from .service import AuthService

auth_router = APIRouter(
    prefix = '/auth'
)

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@auth_router.post("/", status_code=HTTPStatus.CREATED)
async def create_user(create_user_data: CreateUserModel,
                      session: db_dependency):
    new_user = await AuthService(session).create_user(create_user_data)
    return new_user

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: db_dependency):
    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

