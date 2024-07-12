from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import Track
from .schemas import TrackCreateModel

class TrackService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_tracks(self):
        statement = select(Track).order_by(Track.title)
        
        result = await self.session.exec(statement)

        return result.all()
    

    async def create_track(self, track_data: TrackCreateModel):
        new_track = Track(**track_data.model_dump())

        self.session.add(new_track)
        await self.session.commit()
    
        return new_track
    

    async def get_track(self, track_id: int):
        statement = select(Track).where(Track.id == track_id)

        result = await self.session.exec(statement)

        return result.first()
    

    async def update_track(self, track_id: int, track_update_data: TrackCreateModel):
        statement = select(Track).where(Track.id == track_id)

        result = await self.session.exec(statement)
        track = result.first()

        for key, value in track_update_data.model_dump().items():
            setattr(track, key, value)

        await self.session.commit()

    async def delete_track(self, track_id: int):
        statement = select(Track).where(Track.id == track_id)
        result = await self.session.exec(statement)
        track = result.first()
        
        self.session.delete(track)
        await self.session.commit()        
