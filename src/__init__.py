from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.albums.routes import album_router
from src.artists.routes import artist_router
from src.tracks.routes import track_router
from src.auth.routes import auth_router
from src.model_import.routes import import_router
from src.subscriptions.routes import sub_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="music service | interview for zypl.ai",
    lifespan=lifespan
)

app.include_router(album_router, tags=['albums'])
app.include_router(artist_router, tags=['artist'])
app.include_router(track_router, tags=['track'])
app.include_router(auth_router, tags=['auth'])
app.include_router(import_router, tags=['import'])
app.include_router(sub_router, tags=['subscriptions'])