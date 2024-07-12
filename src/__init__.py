from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="music service | interview for zypl.ai",
    lifespan=lifespan
)

@app.get("/")
async def main():
    return {"message": "test"}