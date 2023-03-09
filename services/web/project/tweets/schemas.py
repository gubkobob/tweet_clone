"""
schemas.py
----------
Модуль реализует pydantic-схемы для валидации данных и обмена данных между сервисами.

"""

from typing import List, Optional

from pydantic import BaseModel, Field, validator
from pydantic.schema import Sequence
from sqlalchemy.ext.associationproxy import _AssociationList

from ..users.schemas import AuthorBaseSchema, AuthorLikeSchema


class TweetIn(BaseModel):
    """
    Pydantic-схема ввода данных твита

    Parameters
    ----------
    tweet_data: str
        Содержание твита
    tweet_media_ids: List[int], optional
        Список идентификаторов картинок
    attachments: List[str], optional
        Список вложений
    """

    tweet_data: str
    tweet_media_ids: Optional[List[int]]
    # attachments: Optional[List[str]]

    class Config:
        orm_mode = True


class BaseAnsTweet(BaseModel):
    """
    Pydantic-схема базового вывода ответа о публикации твита

    Parameters
    ----------
    result: bool
        Флаг об успешном добавлении твита
    tweet_id: int
        Идентификатор твита в СУБД

    """

    result: bool
    tweet_id: int


class TweetSchema(BaseModel):
    """
    Pydantic-схема твита для фронтенда

    Parameters
    ----------
    id: int
        Идентификатор твита в СУБД
    content: str = Field(example="супер твит")
        Содержание твита
    attachments: List[str], optional
        Список вложений
    author: AuthorBaseSchema
        Автор твита
    likes: List[AuthorLikeSchema], optional
        Список пользователей, отлайкавших твит
    """

    id: int
    content: str = Field(example="супер твит")
    attachments: Optional[Sequence[str]]
    author: AuthorBaseSchema
    likes: Optional[List[AuthorLikeSchema]]

    @validator("attachments", pre=True, whole=True)
    def check_roles(cls, v):
        if type(v) is _AssociationList or issubclass(cls, Sequence):
            return set(v)
        raise ValueError("not a valid sequence")

    class Config:
        orm_mode = True


class TweetListOutSchema(BaseModel):
    """
    Pydantic-схема списка твитов для фронтенда

    Parameters
    ----------
    result: bool = True
        Флаг успешного выполнения
    tweets: List[TweetSchema], optional
        Список твитов
    """

    result: bool = True
    tweets: Optional[List[TweetSchema]]
