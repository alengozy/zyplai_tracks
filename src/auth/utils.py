from src.db.models import User
from sqlmodel import select
from src.config import settings
from jose import jwt, JWTError
from datetime import timedelta, datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException
from http import HTTPStatus
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer\

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

async def authenticate_user(username: str, password: str, session: AsyncSession):
    statement = select(User).where(User.username == username)

    result = await session.exec(statement)
    user = result.first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username': username, 'id': user_id}
    except JWTError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail='Could not validate user')