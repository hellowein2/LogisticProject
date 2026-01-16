from fastapi import Cookie, HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.parcels import AsyncParcelRepository
from app.services.parcels import ParcelService
from app.repositories.parcel_type import ParcelTypeRepository
from app.services.parcel_type import ParcelTypeService


def get_parcel_service(db: AsyncSession = Depends(get_db)) -> ParcelService:
    return ParcelService(AsyncParcelRepository(db))


def get_parcel_type_service(db: AsyncSession = Depends(get_db)) -> ParcelTypeService:
    return ParcelTypeService(ParcelTypeRepository(db))


def get_session_id(sid: str | None = Cookie(default=None)) -> str:
    if sid is None:
        raise HTTPException(status_code=401, detail='Missing session id')
    return sid