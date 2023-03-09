from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import Media
from ..exeptions import BackendExeption


async def post_image(session: AsyncSession, image_name: str) -> dict:
    q = await session.execute(insert(Media).values(name=image_name))
    image_id = q.inserted_primary_key[0]
    await session.commit()
    return {"result": True, "media_id": image_id}


def check_file(file):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise BackendExeption(
            error_type="BAD FILE", error_message="Bad file type"
        )
