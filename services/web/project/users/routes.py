"""
routes.py
----------
Модуль реализует эндпоинты FastApi для взамодействия с пользователями.

"""
from typing import Union

from fastapi import APIRouter, Depends, Header, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..exeptions import BackendExeption
from ..schemas_overal import ErrorSchema, OnlyResult
from ..users.schemas import UserIn, UserOut, UserResultOutSchema
from ..users.services import (
    delete_follow_to_user,
    get_user,
    get_user_me,
    post_follow_to_user,
    post_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/{id}/follow",
    summary="Отметка следит за другим пользователем",
    response_description="Сообщение о результате",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def post_follow_to_user_handler(
    response: Response,
    id: int,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Эндпоинт публикации отметки 'следит' за другим пользователем

    :param response: Response
         Обьект ответа на запрос
    :param id: int
        Идентификатор пользователя в СУБД
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[OnlyResult, ErrorSchema]
        Pydantic-схема для фронтенда с результатом или ошибкой
    """
    try:
        await post_follow_to_user(session=session, api_key=api_key, user_id=id)
        return {"result": True}
    except BackendExeption as e:
        response.status_code = 404
        return e


@router.delete(
    "/{id}/follow",
    summary="Удаление отметки следит за другим пользователем",
    response_description="Сообщение о результате",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def delete_follow_to_user_handler(
    response: Response,
    id: int,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Эндпоинт удаления отметки 'следит' за другим пользователем

    :param response: Response
         Обьект ответа на запрос
    :param id: int
        Идентификатор пользователя в СУБД
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[OnlyResult, ErrorSchema]
        Pydantic-схема для фронтенда с результатом или ошибкой
    """
    try:
        await delete_follow_to_user(
            session=session, api_key=api_key, user_id=id
        )
        return {"result": True}
    except BackendExeption as e:
        response.status_code = 404
        return e


@router.get(
    "/me",
    summary="Получение информации о пользователе по api-key",
    response_description="Сообщение о результате с данными пользователя",
    response_model=Union[UserResultOutSchema, ErrorSchema],
    status_code=200,
)
async def get_user_me_handler(
    response: Response,
    api_key: str = Header(),
    session: AsyncSession = Depends(get_session),
) -> Union[UserResultOutSchema, ErrorSchema]:
    """
    Эндпоинт получения информации о пльзователе по api-key

    :param response: Response
         Обьект ответа на запрос
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[UserResultOutSchema, ErrorSchema]
        Pydantic-схема для фронтенда с данными пользователя или ошибкой
    """
    try:
        result = await get_user_me(session=session, api_key=api_key)
        return result
    except BackendExeption as e:
        response.status_code = 404
        return e


@router.get(
    "/{id}",
    summary="Получение информации о пользователе по id",
    response_description="Сообщение о результате с данными пользователя",
    response_model=Union[UserResultOutSchema, ErrorSchema],
    status_code=200,
)
async def get_user_by_id_handler(
    response: Response, id: int, session: AsyncSession = Depends(get_session)
) -> Union[UserResultOutSchema, ErrorSchema]:
    """
    Эндпоинт получения информации о пльзователе по его id

    :param response: Response
         Обьект ответа на запрос
    :param id: int
        id пользователя в СУБД
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[UserResultOutSchema, ErrorSchema]
        Pydantic-схема для фронтенда с данными пользователя или ошибкой
    """
    try:
        result = await get_user(session=session, user_id=id)
        return result
    except BackendExeption as e:
        response.status_code = 404
        return e


@router.post(
    "/",
    summary="Регистрация нового пользователя",
    response_description="Сообщение о результате с данными пользователя",
    response_model=UserOut,
)
async def post_users_handler(
    user: UserIn, session: AsyncSession = Depends(get_session)
) -> UserOut:
    """
    Эндпоинт регистрации нового пользователя

    :param user: UserIn
         Данные о пользователе из pydantic-схемы
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: UserOut
        Обьект пользователя - pydantic-схема
    """
    result = await post_user(session=session, user=user)
    return result
