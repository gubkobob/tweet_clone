from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import User, followers
from ..exeptions import BackendExeption
from ..services_overal import get_user_by_api_key


async def post_follow_to_user(
    session: AsyncSession, api_key: str, user_id: int
):
    following_user = await get_user_by_api_key(
        session=session, api_key=api_key
    )
    if following_user.id == user_id:
        raise BackendExeption(
            error_type="BAD FOLLOW", error_message="User can't follow himself"
        )

    q = await session.execute(select(User).where(User.id == user_id))
    user_followed = q.scalars().one_or_none()
    if not user_followed:
        raise BackendExeption(
            error_type="NO USER",
            error_message="No user with user_id to follow",
        )
    try:
        await session.execute(
            insert(followers).values(
                following_user_id=following_user.id,
                followed_user_id=user_id,
            )
        )
    except IntegrityError:
        raise BackendExeption(
            error_type="BAD FOLLOW", error_message="Such follow already exists"
        )
    await session.commit()


async def delete_follow_to_user(
    session: AsyncSession, api_key: str, user_id: int
):
    following_user = await get_user_by_api_key(
        session=session, api_key=api_key
    )
    q = await session.execute(
        select(followers).where(
            followers.c.following_user_id == following_user.id,
            followers.c.followed_user_id == user_id,
        )
    )
    follower = q.scalars().one_or_none()
    if not follower:
        raise BackendExeption(
            error_type="BAD FOLLOW DELETE", error_message="No such follow"
        )

    await session.execute(
        delete(followers).where(
            followers.c.following_user_id == following_user.id,
            followers.c.followed_user_id == user_id,
        )
    )
    await session.commit()


async def get_user_me(session: AsyncSession, api_key: str):
    user = await get_user_by_api_key(session=session, api_key=api_key)

    q = await session.execute(
        select(User)
        .options(selectinload(User.following))
        .options(selectinload(User.followers))
        .where(User.api_key == api_key)
    )

    user = q.scalars().one_or_none()

    return {"result": True, "user": user}


async def get_user(session: AsyncSession, user_id: int):
    q = await session.execute(
        select(User)
        .options(selectinload(User.following))
        .options(selectinload(User.followers))
        .where(User.id == user_id)
    )

    user = q.scalars().one_or_none()
    if not user:
        raise BackendExeption(
            error_type="NO USER", error_message="No user with such id"
        )

    return {"result": True, "user": user}


async def post_user(session: AsyncSession, user) -> User:
    new_user = User(**user.dict())
    async with session.begin():
        session.add(new_user)
        await session.commit()
    return new_user
