from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import Album
from .schemas import AlbumCreateModel

class AlbumService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_albums(self):
        statement = select(Album).order_by(Album.title)
        
        result = await self.session.exec(statement)

        return result.all()
    

    async def create_album(self, album_data: AlbumCreateModel):
        new_album = Album(**album_data.model_dump())

        self.session.add(new_album)
        await self.session.commit()
    
        return new_album
    

    async def get_album(self, album_id: int):
        statement = select(Album).where(Album.id == album_id)

        result = await self.session.exec(statement)

        return result.first()
    

    async def update_album(self, album_id: int, album_update_data: AlbumCreateModel):
        statement = select(Album).where(Album.id == album_id)

        result = await self.session.exec(statement)
        album = result.first()

        for key, value in album_update_data.model_dump().items():
            setattr(album, key, value)

        await self.session.commit()

    async def delete_album(self, album_id: int):
        statement = select(Album).where(Album.id == album_id)
        result = await self.session.exec(statement)
        album = result.first()
        
        self.session.delete(album)
        await self.session.commit()