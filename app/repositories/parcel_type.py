from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.db.models import ParcelType


class ParcelTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self) -> list[ParcelType]:
        result = await self.db.execute(select(ParcelType))
        return result.scalars().all()


class SyncParcelTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def parcel_type_exists(self, type_id: int) -> bool:
        stmt = select(ParcelType.id).where(ParcelType.id == type_id)
        return self.db.execute(stmt).scalar_one_or_none() is not None