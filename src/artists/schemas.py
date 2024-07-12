from src.db.models import Artist
from pydantic import BaseModel

class ArtistResponseModel(BaseModel):
    id: int
    name: str


class ArtistCreateModel(ArtistResponseModel):
    pass

class ArtistImportModel(ArtistResponseModel):
    pass
