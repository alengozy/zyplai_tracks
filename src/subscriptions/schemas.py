from pydantic import BaseModel
from src.db.models import Subscription

class SubscribeResponseModel(Subscription):
    pass

class SubsciptionModel(BaseModel):
    artist_id: int
