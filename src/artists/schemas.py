from src.db.models import Artist
from pydantic import BaseModel

class ArtistResponseModel(Artist):
    pass

class ArtistCreateModel(BaseModel):
    id: int
    name: str
