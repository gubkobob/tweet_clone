"""
routes.py
----------
Модуль реализует эндпоинты FastApi для взамодействия с картинками.

"""
from pathlib import Path
from typing import Union

import aiofiles
from fastapi import APIRouter, Depends, Header, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..exeptions import BackendExeption
from ..media.schemas import MediaOutSchema
from ..media.services import check_file, post_image
from ..schemas_overal import ErrorSchema

router = APIRouter(prefix="/medias", tags=["Medias"])

OUT_PATH = Path(__file__).parent / "media_files"
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


PREFIX_NAME = "/static/media_files/"
# OUT_PATH.mkdir(exist_ok=True, parents=True)
@router.post(
    "/",
    summary="Загрузка изображений для твита",
    response_description="Сообщение о результате",
    response_model=Union[MediaOutSchema, ErrorSchema],
    status_code=200,
)
async def post_image_handler(
    response: Response,
    file: UploadFile,
    api_key: str = Header(),
    session: AsyncSession = Depends(get_session),
) -> Union[MediaOutSchema, ErrorSchema]:
    """
    Эндпоинт загрузки изображений для твита

    :param response: Response
         Обьект ответа на запрос
    :param file: UploadFile
        Файл с картинкой
    :param api_key: str
        api-key пользователя
    :param session: Asyncsession
        Экземпляр сессии из sqlalchemy

    :return: Union[MediaOutSchema, ErrorSchema]
        Pydantic-схема для фронтенда с результатом или ошибкой
    """
    try:
        check_file(file)

        filename = file.filename
        file_data = await file.read()
        path = "{}/{}".format(OUT_PATH, filename)
        async with aiofiles.open(path, mode="wb") as some_file:
            await some_file.write(file_data)

        name_for_db = PREFIX_NAME + filename

        result = await post_image(session=session, image_name=name_for_db)
        return result
    except BackendExeption as e:
        response.status_code = 400
        return e
