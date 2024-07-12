from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Subscription, Artist
from .schemas import SubsciptionModel
from sqlmodel import select

class SubscribeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def subscribe(self, user_id: int, new_sub_data: SubsciptionModel):
        new_subscription = Subscription(user_id=user_id, 
                                        artist_id=new_sub_data.artist_id)
        self.session.add(new_subscription)
        await self.session.commit()

        return new_subscription

    async def unsubscribe(self, user_id: int, unsub_data: SubsciptionModel): 
        statement = select(Subscription).where((Subscription.artist_id == unsub_data.artist_id) &
                                               (Subscription.user_id == user_id))
        result = await self.session.exec(statement)
        subscription = result.first()
        
        self.session.delete(subscription)
        await self.session.commit()



        
