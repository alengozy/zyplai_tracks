from sqlmodel import SQLModel, Field
from datetime import datetime

class Artist(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    name: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)

class Album(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    title: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)
    
    artist_id: int = Field(foreign_key="artist.id")

class Track(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    
    title: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)

    artist_id: int = Field(foreign_key="artist.id")
    album_id: int = Field(foreign_key="album.id", default=None) #nullable альбом для синглов
    
