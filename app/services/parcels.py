from uuid import UUID

from app.repositories.parcels import AsyncParcelRepository
from app.schemas.parcels import ParcelListOut, ParcelOut, ParcelDetailOut
from app.exceptions.parcels import ParcelNotFoundError


class ParcelService:

    def __init__(self, repo: AsyncParcelRepository):
        self.repo = repo

    @staticmethod
    def _to_parcel_detail(parcel) -> ParcelDetailOut:
        return ParcelDetailOut(
            name=parcel.name,
            weight=float(parcel.weight),
            parcel_type_id=parcel.parcel_type_id,
            type_name=parcel.parcel_type.name,
            content_price_usd=float(parcel.content_price_usd),
            delivery_price_rub=(
                parcel.delivery_price_rub
                if parcel.delivery_price_rub is not None
                else "Не рассчитано"),
        )

    @staticmethod
    def _require_parcel(parcel):
        if parcel is None:
            raise ParcelNotFoundError()
        return parcel


    async def list_parcels(
        self,
        session_id: str,
        page: int,
        page_size: int,
        type_id: int | None,
        has_delivery_cost: bool | None,
    ) -> ParcelListOut:
        items, total = await self.repo.list_by_session(
            session_id=session_id,
            page=page,
            page_size=page_size,
            type_id=type_id,
            has_delivery_cost=has_delivery_cost,
        )

        dto_items: list[ParcelOut] = []
        for p in items:
            dto_items.append(
                ParcelOut(
                    id=p.id,
                    public_id=p.public_id,
                    name=p.name,
                    weight=float(p.weight),
                    parcel_type_id=p.parcel_type_id,
                    type_name=p.parcel_type.name,
                    content_price_usd=float(p.content_price_usd),
                    delivery_price_rub=(
                        p.delivery_price_rub
                    if p.delivery_price_rub is not None
                        else "Не рассчитано")
                )
            )

        return ParcelListOut(
            items=dto_items,
            page=page,
            page_size=page_size,
            total=total,
        )

    async def get_parcel_by_id(self, *, parcel_id: int, session_id: str) -> ParcelDetailOut:
        parcel = await self.repo.get_by_id_for_session(parcel_id=parcel_id, session_id=session_id)
        parcel = self._require_parcel(parcel)
        return self._to_parcel_detail(parcel)

    async def get_parcel_by_public_id(self, *, public_id: UUID, session_id: str) -> ParcelDetailOut:
        parcel = await self.repo.get_by_public_id(public_id=public_id, session_id=session_id)
        parcel = self._require_parcel(parcel)
        return self._to_parcel_detail(parcel)