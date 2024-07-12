from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from http import HTTPStatus
from .service import ArtistService
from .schemas import ArtistCreateModel, ArtistResponseModel
artist_router = APIRouter(
    prefix="/artists"
)

@artist_router.get("/",
                   status_code=HTTPStatus.OK,
                   response_model=ArtistResponseModel
                   )
async def get_artists(session: AsyncSession = Depends(get_session)):
    artists = await ArtistService.get_all_artists(session=session)
    return artists

@artist_router.post("/", status_code=HTTPStatus.CREATED)
async def create_artist(artist_create_data: ArtistCreateModel,
                        session: AsyncSession = Depends(get_session)):
    new_artist = await ArtistService(session).create_artist(artist_create_data)
    return new_artist

@artist_router.get("/{artist_id}", status_code=HTTPStatus.OK)
async def get_artist(artist_id: int,
                    session: AsyncSession = Depends(get_session)):
    artist = await ArtistService(session).get_artist(artist_id)
    return artist

@artist_router.put("/{artist_id}", status_code=HTTPStatus.OK)
async def update_artist(artist_id: int,
                       artist_update_data: ArtistCreateModel,
                       session: AsyncSession = Depends(get_session)):
    updated_artist = await ArtistService(session).update_artist(artist_id, artist_update_data)
    return updated_artist

@artist_router.delete("/{artist_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_artist(artist_id: int,
                       session: AsyncSession = Depends(get_session)):
    await ArtistService(session).delete_artist(artist_id)
    return {}