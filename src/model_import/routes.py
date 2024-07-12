
import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from typing import Annotated
from src.auth.utils import get_current_user
from .utils import convert_to_model_objects

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]


import_router = APIRouter(
    prefix="/import"
)

@import_router.post("/import_artists")
async def import_objects(user: user_dependency, session: db_dependency, csv_file: UploadFile = File(...)):
    try:
        df = pd.read_csv(csv_file.file)
        model_objects = convert_to_model_objects(df)

        for obj in model_objects:
            session.add(obj)
        await session.commit()
        return {"message": "Objects imported successfully"}
    except ValueError as e:
        return {"error": str(e)}