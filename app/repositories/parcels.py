from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload, Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Parcel

from uuid import UUID


class AsyncParcelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_session(
            self,
            session_id: str,
            page: int,
            page_size: int,
            type_id: int | None,
            has_delivery_cost: bool | None,
    ) -> tuple[list[Parcel], int]:

        stmt = (
            select(Parcel)
            .where(Parcel.session_id == session_id)
            .options(selectinload(Parcel.parcel_type))
        )

        if type_id is not None:
            stmt = stmt.where(Parcel.parcel_type_id == type_id)

        if has_delivery_cost is True:
            stmt = stmt.where(Parcel.delivery_price_rub.is_not(None))
        elif has_delivery_cost is False:
            stmt = stmt.where(Parcel.delivery_price_rub.is_(None))

        stmt = stmt.order_by(desc(Parcel.id))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        items = (await self.db.execute(stmt)).scalars().all()

        return items, total

    async def get_by_id_for_session(self, *, parcel_id: int, session_id: str) -> Parcel | None:
        stmt = select(Parcel).where(
            Parcel.id == parcel_id,
            Parcel.session_id == session_id,
        ).options(selectinload(Parcel.parcel_type))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, *, session_id: str, public_id: UUID) -> Parcel | None:
        stmt = (
            select(Parcel)
            .where(Parcel.session_id == session_id, Parcel.public_id == public_id)
            .options(selectinload(Parcel.parcel_type))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

class SyncParcelRepository:
    def __init__(self, db: Session):
        self.db = db


    def create(
            self,
            *,
            public_id: UUID,
            session_id: str,
            name: str,
            weight: float,
            parcel_type_id: int,
            content_price_usd: float,
            delivery_price_rub: float,
    ) -> Parcel:
        obj = Parcel(
            public_id=public_id,
            session_id=session_id,
            name=name,
            weight=weight,
            parcel_type_id=parcel_type_id,
            content_price_usd=content_price_usd,
            delivery_price_rub=delivery_price_rub,
        )
        self.db.add(obj)
        return obj
