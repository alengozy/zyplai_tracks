from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from http import HTTPStatus
from .service import TrackService
from .schemas import TrackCreateModel, TrackResponseModel
track_router = APIRouter(
    prefix="/tracks"
)

@track_router.get("/",
                   status_code=HTTPStatus.OK,
                   response_model=TrackResponseModel
                   )
async def get_tracks(session: AsyncSession = Depends(get_session)):
    tracks = await TrackService.get_all_tracks(session=session)
    return tracks

@track_router.post("/", status_code=HTTPStatus.CREATED)
async def create_track(track_create_data: TrackCreateModel,
                        session: AsyncSession = Depends(get_session)):
    new_track = await TrackService(session).create_track(track_create_data)
    return new_track

@track_router.get("/{track_id}", status_code=HTTPStatus.OK)
async def get_track(track_id: int,
                    session: AsyncSession = Depends(get_session)):
    track = await TrackService(session).get_track(track_id)
    return track

@track_router.put("/{track_id}", status_code=HTTPStatus.OK)
async def update_track(track_id: int,
                       track_update_data: TrackCreateModel,
                       session: AsyncSession = Depends(get_session)):
    updated_track = await TrackService(session).update_track(track_id, track_update_data)
    return updated_track

@track_router.delete("/{track_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_track(track_id: int,
                       session: AsyncSession = Depends(get_session)):
    await TrackService(session).delete_track(track_id)
    return {}