from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from http import HTTPStatus
from .service import AlbumService
from .schemas import AlbumCreateModel, AlbumResponseModel
from typing import Annotated
from src.auth.utils import get_current_user

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]

album_router = APIRouter(
    prefix="/albums"
)

@album_router.get("/",
                  status_code=HTTPStatus.OK,
                  response_model=AlbumResponseModel)
async def get_albums(user: user_dependency, session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')

    albums = await AlbumService(session).get_all_albums()
    return albums

@album_router.post("/", status_code=HTTPStatus.CREATED)
async def create_album(
    album_create_data: AlbumCreateModel,
    user: user_dependency,
    session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    new_album = await AlbumService(session).create_album(album_create_data)
    return new_album

@album_router.get("/{album_id}", status_code=HTTPStatus.OK)
async def get_album(album_id: int,
                    user: user_dependency,
                    session:db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    album = await AlbumService(session).get_album(album_id)
    return album

@album_router.put("/{album_id}", status_code=HTTPStatus.OK)
async def update_album(album_id: int,
                       album_update_data: AlbumCreateModel,
                       user: user_dependency,
                       session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')

    updated_album = await AlbumService(session).update_album(album_id, album_update_data)
    return updated_album

@album_router.delete("/{album_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_album(album_id: int,
                       user: user_dependency,
                       session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    await AlbumService(session).delete_album(album_id)
    return {}
