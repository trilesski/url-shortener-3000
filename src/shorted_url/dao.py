import logging

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import BaseDAO
from src.shorted_url.models import ShortedUrl

logger = logging.getLogger()


class ShortedUrlDAO(BaseDAO):
    model = ShortedUrl

    @classmethod
    async def inc_visits_count(cls, session: AsyncSession, short_id: str):
        result = await session.execute(select(cls.model).filter_by(short_id=short_id).with_for_update())
        obj = result.scalars().first()

        if not obj:
            raise NoResultFound()

        obj.visits += 1
        await session.commit()

        return obj
