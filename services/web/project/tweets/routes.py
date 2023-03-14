"""
routes.py
----------
Модуль реализует эндпоинты FastApi для взамодействия с твитами.

"""

from typing import Union

from fastapi import APIRouter, Depends, Header, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..exeptions import BackendExeption
from ..schemas_overal import ErrorSchema, OnlyResult
from ..tweets.schemas import (
    BaseAnsTweet,
    TweetIn,
    TweetListOutSchema,
    TweetSchema,
)
from ..tweets.services import (
    delete_like_to_tweet,
    delete_tweet,
    get_tweet,
    get_tweets,
    insert_media_to_tweet,
    post_like_to_tweet,
    post_tweet,
)

router = APIRouter(prefix="/tweets", tags=["Tweets"])


@router.get(
    "/{id}",
    summary="Получение твита по id",
    response_description="Сообщение о результате",
    response_model=Union[TweetSchema, ErrorSchema],
    status_code=200,
)
async def get_tweet_handler(
    response: Response, id: int, session: AsyncSession = Depends(get_session)
) -> Union[TweetSchema, ErrorSchema]:
    """
    Эндпоинт возвращает твит по идентификатору или сообщение об ошибке
    \f
    :param response: Response
         Обьект ответа на запрос
    :param id: int
        Идентификатор твита в БД
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[TweetSchema, ErrorSchema]
        Pydantic-схема для фронтенда с твитом или ошибкой
    """

    try:
        result = await get_tweet(session=session, tweet_id=id)
    except BackendExeption as e:
        response.status_code = 404
        result = e

    return result


@router.get(
    "/",
    summary="Получение твитов юзера по api-key",
    response_description="Сообщение о результате со списком твитов",
    response_model=Union[TweetListOutSchema, ErrorSchema],
    status_code=200,
)
async def get_tweets_handler(
    response: Response,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[TweetListOutSchema, ErrorSchema]:
    """
    Эндпоинт возвращает твиты пользователя по api-key или сообщение об ошибке
    \f
    :param response: Response
         Обьект ответа на запрос
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[TweetListOutSchema, ErrorSchema]
        Pydantic-схема для фронтенда с твитами пользователя или ошибкой
    """

    try:
        result = await get_tweets(session=session, api_key=api_key)
    except BackendExeption as e:
        response.status_code = 404
        result = e

    return result


@router.post(
    "/",
    summary="Публикация твита",
    response_description="Сообщение о результате",
    response_model=Union[BaseAnsTweet, ErrorSchema],
    status_code=200,
)
async def post_tweets_handler(
    response: Response,
    tweet: TweetIn,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[BaseAnsTweet, ErrorSchema]:
    """
    Эндпоинт публикации твита пользователя по его api-key
    \f
    :param response: Response
         Обьект ответа на запрос
    :param tweet: TweetIn
        данные твита из pedantic-схемы ввода данных
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[BaseAnsTweet, ErrorSchema]
        Pydantic-схема для фронтенда с флагом об удачной операции или ошибкой
    """
    try:
        new_tweet_id = await post_tweet(
            session=session, api_key=api_key, tweet_data=tweet.tweet_data
        )
        if tweet.tweet_media_ids:
            await insert_media_to_tweet(
                session=session,
                tweet_id=new_tweet_id,
                tweet_medias=tweet.tweet_media_ids,
            )
        return {"result": True, "tweet_id": new_tweet_id}

    except BackendExeption as e:
        response.status_code = 404
        return e


@router.delete(
    "/{id}",
    summary="Удаление твита",
    response_description="Сообщение о результате",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def delete_tweets_handler(
    response: Response,
    id: int,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Эндпоинт удаления твита пользователя по его api-key и id твита
    \f
    :param response: Response
         Обьект ответа на запрос
    :param id: int
        Идентификатор твита в СУБД
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[OnlyResult, ErrorSchema]
        Pydantic-схема для фронтенда с флагом об удачной операции или ошибкой
    """
    try:
        await delete_tweet(session=session, api_key=api_key, tweet_id=id)
        return {"result": True}
    except BackendExeption as e:
        response.status_code = 404
        return e


@router.post(
    "/{id}/likes",
    summary="Отметка лайк к твиту",
    response_description="Сообщение о результате",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def post_like_to_tweet_handler(
    response: Response,
    id: int,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Эндпоинт регистрации лайка к твиту по api-key и id твита
    \f
    :param response: Response
         Обьект ответа на запрос
    :param id: int
        Идентификатор твита в СУБД
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[OnlyResult, ErrorSchema]
        Pydantic-схема для фронтенда с флагом об удачной операции или ошибкой
    """
    try:
        await post_like_to_tweet(session=session, api_key=api_key, tweet_id=id)
        return {"result": True}
    except BackendExeption as e:
        response.status_code = 404
        return e


@router.delete(
    "/{id}/likes",
    summary="Удаление отметки лайк к твиту",
    response_description="Сообщение о результате",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def delete_like_to_tweet_handler(
    response: Response,
    id: int,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Эндпоинт удаления лайка к твиту по api-key и id твита
    \f
    :param response: Response
         Обьект ответа на запрос
    :param id: int
        Идентификатор твита в СУБД
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[OnlyResult, ErrorSchema]
        Pydantic-схема для фронтенда с флагом об удачной операции или ошибкой
    """
    try:
        await delete_like_to_tweet(
            session=session, api_key=api_key, tweet_id=id
        )
        return {"result": True}
    except BackendExeption as e:
        response.status_code = 404
        return e
