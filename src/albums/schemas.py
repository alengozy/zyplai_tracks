from src.db.models import Album, Artist, Track
from pydantic import BaseModel

class AlbumResponseModel(Album):
    pass

class AlbumCreateModel(BaseModel):
    id: int
    title: str
    artist_id: int