from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from .schemas import CreateUserModel
from .utils import bcrypt_context

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, create_user_data: CreateUserModel):
        new_user = User(username=create_user_data.username,
                                email=create_user_data.email,
                                hashed_password=bcrypt_context.hash(create_user_data.password))
        self.session.add(new_user)
        await self.session.commit()

        return new_user
