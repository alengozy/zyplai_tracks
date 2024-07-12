from src.db.models import Track
from pydantic import BaseModel

class TrackResponseModel(Track):
    pass

class TrackCreateModel(BaseModel):
    id: int
    title: str
    artist_id: int
    album_id: int = None