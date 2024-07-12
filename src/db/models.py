from sqlmodel import SQLModel, Field, Relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Subscription(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    artist_id: int = Field(default=None, foreign_key="artist.id", primary_key=True)


class Artist(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    
    subscribers: list["User"] = Relationship(back_populates="subscriptions", link_model=Subscription)


class Album(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, nullable=False)

    artist_id: int = Field(foreign_key="artist.id")


class Track(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, nullable=False)

    artist_id: int = Field(foreign_key="artist.id")
    album_id: int = Field(foreign_key="album.id", default=None) #nullable альбом для синглов
    

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=50, nullable=False)
    email: str = Field(unique=True, nullable=True)
    hashed_password: str = Field(nullable=False)
    
    subscriptions: list["Artist"] = Relationship(back_populates="subscribers", link_model=Subscription)
