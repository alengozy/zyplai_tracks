from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import Artist
from .schemas import ArtistCreateModel

class ArtistService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_artists(self):
        statement = select(Artist).order_by(Artist.name)
        
        result = await self.session.exec(statement)

        return result.all()
    
    async def create_artist(self, artist_data: ArtistCreateModel):
        new_artist = Artist(**artist_data.model_dump())

        self.session.add(new_artist)
        await self.session.commit()
    
        return new_artist


    async def get_artist(self, artist_id: int):
        statement = select(Artist).where(Artist.id == artist_id)

        result = await self.session.exec(statement)

        return result.first()
    

    async def update_artist(self, artist_id: int, artist_update_data: ArtistCreateModel):
        statement = select(Artist).where(Artist.id == artist_id)

        result = await self.session.exec(statement)
        artist = result.first()

        for key, value in artist_update_data.model_dump().items():
            setattr(artist, key, value)

        await self.session.commit()

    async def delete_artist(self, artist_id: int):
        statement = select(Artist).where(Artist.id == artist_id)
        result = await self.session.exec(statement)
        artist = result.first()
        
        self.session.delete(artist)
        await self.session.commit()

    async def get_subscribed_users(self, artist_id: int):
        statement = select(Artist.subscribers).where(Artist.id == artist_id)
        result = await self.session.exec(statement)

        return result.all()