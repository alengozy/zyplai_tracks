from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from http import HTTPStatus
from .service import ArtistService
from .schemas import ArtistCreateModel, ArtistResponseModel
from typing import Annotated
from src.auth.utils import get_current_user

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]


artist_router = APIRouter(
    prefix="/artists"
)

@artist_router.get("/",
                   status_code=HTTPStatus.OK,
                   response_model=ArtistResponseModel
                   )
async def get_artists(user: user_dependency, session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')

    artists = await ArtistService(session).get_all_artists()
    return artists

@artist_router.post("/", status_code=HTTPStatus.CREATED)
async def create_artist(artist_create_data: ArtistCreateModel,
                        user: user_dependency,
                        session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    new_artist = await ArtistService(session).create_artist(artist_create_data)
    return new_artist

@artist_router.get("/{artist_id}", status_code=HTTPStatus.OK)
async def get_artist(artist_id: int,
                     user: user_dependency,
                     session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    artist = await ArtistService(session).get_artist(artist_id)
    return artist

@artist_router.put("/{artist_id}", status_code=HTTPStatus.OK)
async def update_artist(artist_id: int,
                        artist_update_data: ArtistCreateModel,
                        user: user_dependency,
                        session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    updated_artist = await ArtistService(session).update_artist(artist_id, artist_update_data)
    return updated_artist

@artist_router.delete("/{artist_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_artist(artist_id: int,
                        user: user_dependency,
                        session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')

    await ArtistService(session).delete_artist(artist_id)
    return {}