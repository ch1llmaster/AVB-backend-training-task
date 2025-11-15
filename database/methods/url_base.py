from sqlalchemy import select

from database.db_async import async_session
from database.models import URLBase


async def create_new_record(default_url: str, uniq_id: str, shortened_url: str) -> URLBase:
    async with async_session() as session:
        url_record = URLBase(default_url=default_url, uniq_id=uniq_id, shortened_url=shortened_url)
        session.add(url_record)
        await session.commit()
        return url_record


async def get_record_by_uniq_id(uniq_id: str) -> URLBase | None:
    async with async_session() as session:
        query = select(URLBase).where(URLBase.uniq_id == uniq_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
