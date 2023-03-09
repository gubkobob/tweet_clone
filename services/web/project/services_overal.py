from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import User
from .exeptions import BackendExeption


async def get_user_by_api_key(session: AsyncSession, api_key: str) -> User:
    q = await session.execute(select(User).where(User.api_key == api_key))
    user = q.scalars().one_or_none()

    if not user:
        raise BackendExeption(
            error_type="NO USER", error_message="No user with such api-key"
        )

    return user
