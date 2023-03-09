"""
schemas.py
----------
Модуль реализует pydantic-схемы для валидации данных
и обмена данных между сервисами.

"""

from typing import List, Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    """
    Базовая Pydantic-схема пользователя

    Parameters
    ----------
    api_key: str
        api_key пользователя
    name: str
        Имя пользователя
    password: str, optional
        Пароль аккаунта пользователя
    """

    api_key: str
    name: str
    password: Optional[str]


class UserIn(BaseUser):
    """
    Pydantic-схема пользователя для ввода данных
    """

    ...


class UserOut(BaseUser):
    """
    Pydantic-схема для вывода данных о пользователе

    Parameters
    ----------
    id: int
        Идентификатор пользователя в СУБД
    """

    id: int

    class Config:
        orm_mode = True


class AuthorBaseSchema(BaseModel):
    """
    Базовая Pydantic-схема автора

    Parameters
    ----------
    id: int
        Идентификатор пользователя в СУБД
    name: str
        Имя пользователя
    """

    id: int
    name: str

    class Config:
        orm_mode = True


class AuthorLikeSchema(BaseModel):
    """
    Базовая Pydantic-схема автора для лайков

    Parameters
    ----------
    user_id: int
        Идентификатор пользователя в СУБД
    name: str
        Имя пользователя
    """

    user_id: int
    name: str

    class Config:
        orm_mode = True


class UserOutSchema(BaseModel):
    """
    Pydantic-схема пользователя для фронтенда

    Parameters
    ----------
    id: int
        Идентификатор пользователя в СУБД
    name: str
        Имя пользователя
    followers: List[AuthorBaseSchema], optional
        Список пользователей, которые следят за автором
    following: List[AuthorBaseSchema], optional
        Список пользователей, за которыми следит автор
    """

    id: int
    name: str
    followers: Optional[List[AuthorBaseSchema]]
    following: Optional[List[AuthorBaseSchema]]

    class Config:
        orm_mode = True


class UserResultOutSchema(BaseModel):
    """
    Pydantic-схема результата о поиске пользователя

    Parameters
    ----------
    result: bool = True
        Флаг о корректном завершении запроса
    user: UserOutSchema
        Информация о пользователе
    """

    result: bool = True
    user: UserOutSchema

    class Config:
        orm_mode = True
