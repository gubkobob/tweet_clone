from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import Like, Media, Tweet, User
from ..exeptions import BackendExeption
from ..services_overal import get_user_by_api_key


async def get_tweet(session: AsyncSession, tweet_id: int):
    q = await session.execute(
        select(Tweet)
        .options(selectinload(Tweet.author))
        .options(selectinload(Tweet.likes).options(selectinload(Like.user)))
        .options(selectinload(Tweet.media))
        .where(Tweet.id == tweet_id)
    )
    tweet = q.scalars().one_or_none()
    if not tweet:
        raise BackendExeption(
            error_type="NO TWEET", error_message="No tweet with such id"
        )
    return tweet


async def get_tweets(session: AsyncSession, api_key: str):
    await get_user_by_api_key(session=session, api_key=api_key)

    q = await session.execute(
        select(Tweet)
        .options(selectinload(Tweet.author))
        .options(selectinload(Tweet.likes).options(selectinload(Like.user)))
        .options(selectinload(Tweet.media))
        .where(Tweet.author.has(User.api_key == api_key))
    )

    tweets = q.scalars().all()

    return {"result": True, "tweets": tweets}


async def post_tweet(
    session: AsyncSession, api_key: str, tweet_data: str
) -> int:
    user = await get_user_by_api_key(session=session, api_key=api_key)

    insert_tweet_query = await session.execute(
        insert(Tweet).values(
            content=tweet_data,
            user_id=user.id,
        )
    )
    new_tweet_id = insert_tweet_query.inserted_primary_key[0]
    await session.commit()

    return new_tweet_id


async def insert_media_to_tweet(
    session: AsyncSession, tweet_id: int, tweet_medias: list
):
    for media_id in tweet_medias:
        await session.execute(
            update(Media).where(Media.id == media_id).values(tweet_id=tweet_id)
        )
        await session.commit()


async def delete_tweet(session: AsyncSession, api_key: str, tweet_id: int):
    user = await get_user_by_api_key(session=session, api_key=api_key)
    await get_tweet(session=session, tweet_id=tweet_id)

    q1 = await session.execute(
        select(Tweet.user_id).where(Tweet.id == tweet_id)
    )
    author_id = q1.scalars().one_or_none()
    if author_id != user.id:
        raise BackendExeption(
            error_type="NO ACCSESS",
            error_message="Tweet belongs to other user",
        )

    await session.execute(
        delete(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user.id)
    )
    await session.commit()


async def post_like_to_tweet(
    session: AsyncSession, api_key: str, tweet_id: int
):
    user = await get_user_by_api_key(session=session, api_key=api_key)
    await get_tweet(session=session, tweet_id=tweet_id)

    try:
        insert_like_query = await session.execute(
            insert(Like).values(
                tweet_id=tweet_id,
                user_id=user.id,
            )
        )
        new_like_id = insert_like_query.inserted_primary_key[0]
        await session.commit()
    except IntegrityError:
        raise BackendExeption(
            error_type="BAD LIKE", error_message="Such like already exists"
        )

    return new_like_id


async def delete_like_to_tweet(
    session: AsyncSession, api_key: str, tweet_id: int
):
    user = await get_user_by_api_key(session=session, api_key=api_key)
    tweet = await get_tweet(session=session, tweet_id=tweet_id)
    q = await session.execute(
        select(Like)
        .where(Like.user_id == user.id)
        .where(Like.tweet_id == tweet.id)
    )
    like = q.scalars().one_or_none()
    if not like:
        raise BackendExeption(
            error_type="BAD LIKE DELETE",
            error_message="No like for tweet from user",
        )

    await session.execute(
        delete(Like).where(Like.tweet_id == tweet_id, Like.user_id == user.id)
    )
    await session.commit()
