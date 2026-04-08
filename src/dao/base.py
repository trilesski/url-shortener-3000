import logging

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger()


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session: AsyncSession, **kwargs):
        instance = cls.model(**kwargs)
        try:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance
        except Exception as exc:
            await session.rollback()
            logger.error(f"Fail {cls.__name__}.add object: {exc}")
            raise exc

    @classmethod
    async def get_or_create(cls, session: AsyncSession, defaults=None, **kwargs):
        stmt = select(cls.model).filter_by(**kwargs)
        obj, is_created = await session.scalar(stmt), False

        if not obj:
            if defaults is not None:
                kwargs.update(defaults)
            try:
                obj, is_created = await cls.add(session, **kwargs), True
            except IntegrityError as exc:
                logger.error(f"Fail {cls.model.__name__}.get_or_create object: {exc}")
                obj, is_created = await session.scalar(stmt), False

        return obj, is_created

    @classmethod
    async def get_filtered(cls, session: AsyncSession, *filters):
        stmt = select(cls.model).where(*filters)
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()

        if not obj:
            raise NoResultFound()

        return obj

