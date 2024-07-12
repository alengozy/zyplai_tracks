from src.db.models import Artist
from pydantic import BaseModel

class ArtistResponseModel(Artist):
    pass

class ArtistCreateModel(BaseModel):
    name: str
