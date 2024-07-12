from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from http import HTTPStatus
from .service import SubscribeService
from .schemas import SubsciptionModel, SubscribeResponseModel
from typing import Annotated
from src.auth.utils import get_current_user

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]


sub_router = APIRouter(
    prefix="/subscription"
)


@sub_router.post("/", status_code=HTTPStatus.CREATED)
async def subscribe(subscribe_data: SubsciptionModel,
                    user: user_dependency,
                    session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')
    
    new_subscription = await SubscribeService(session).subscribe(user.id, subscribe_data)
    return new_subscription



@sub_router.delete("/{artist_id}", status_code=HTTPStatus.NO_CONTENT)
async def unsubscripe(subscribe_data: SubsciptionModel,
                      user: user_dependency,
                      session: db_dependency):
    if not user:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED,
                            detail='Could not validate user')

    await SubscribeService(session).unsubscribe(user.id, subscribe_data)
    return {}