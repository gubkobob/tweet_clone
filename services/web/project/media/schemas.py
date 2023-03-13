"""
schemas.py
----------
Модуль реализует pydantic-схемы для валидации данных
и обмена данных между сервисами.

"""

from pydantic import BaseModel


class MediaOutSchema(BaseModel):
    """
    Pydantic-схема вывода картинки для фронтенда

    Parameters
    ----------
    result: bool
        Флаг успешного выполнения операции
    media_id: int
        Идентификатор ресурса в СУБД
    """

    result: bool = True
    media_id: int

    class Config:
        orm_mode = True
