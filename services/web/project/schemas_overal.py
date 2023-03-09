"""
schemas.py
----------
Модуль реализует pydantic-схемы для валидации данных и обмена данных между сервисами.

"""

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """
    Pydantic-схема ошибки бекенда

    Parameters
    ----------
    result: bool
        Флаг не успешного выполнения операции
    error_type: str
        Тип ошибки
    error_message: str
        Сообщение об ошибке
    """

    result: bool = False
    error_type: str
    error_message: str

    class Config:
        orm_mode = True


class OnlyResult(BaseModel):
    """
    Pydantic-схема выдачи только результата выполнения операции

    Parameters
    ----------
    result: bool
        Флаг выполнения операции
    """

    result: bool
