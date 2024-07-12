from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from http import HTTPStatus

from zyplai_tracks.src.artists.service import ArtistService
from .service import TrackService
from .schemas import TrackCreateModel, TrackResponseModel
from typing import Annotated
from src.auth.utils import get_current_user
from src.subscriptions.utils import send_email_notification

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]

track_router = APIRouter(
    prefix="/tracks"
)

@track_router.get("/",
                   status_code=HTTPStatus.OK,
                   response_model=TrackResponseModel
                   )
async def get_tracks(user: user_dependency, session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')    
    tracks = await TrackService(session).get_all_tracks()
    return tracks

@track_router.post("/", status_code=HTTPStatus.CREATED)
async def create_track(track_create_data: TrackCreateModel,
                       user: user_dependency,
                       session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    new_track = await TrackService(session).create_track(track_create_data)
    subscribed_users = await ArtistService(session).get_subscribed_users(new_track.artist_id)
    
    for user in subscribed_users:
        send_email_notification(new_track, user.email)
    return new_track

@track_router.get("/{track_id}", status_code=HTTPStatus.OK)
async def get_track(track_id: int,
                    user: user_dependency,
                    session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    track = await TrackService(session).get_track(track_id)
    return track

@track_router.put("/{track_id}", status_code=HTTPStatus.OK)
async def update_track(track_id: int,
                       track_update_data: TrackCreateModel,
                       user: user_dependency,
                       session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    updated_track = await TrackService(session).update_track(track_id, track_update_data)
    return updated_track

@track_router.delete("/{track_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_track(track_id: int,
                       user: user_dependency,
                       session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    await TrackService(session).delete_track(track_id)
    return {}