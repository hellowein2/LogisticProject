from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(slots=True)
class FakeParcelType:
    name: str


@dataclass(slots=True)
class FakeParcel:
    id: int
    public_id: UUID
    name: str
    weight: float
    parcel_type_id: int
    parcel_type: FakeParcelType
    content_price_usd: float
    delivery_price_rub: int | None


def parcel_factory(
    *,
    id: int = 1,
    type_name: str = "electronics",
    delivery_price_rub: int | None = 1500,
    name: str = "Box",
    weight: float = 10.0,
    parcel_type_id: int = 2,
    content_price_usd: float = 200.0,
    public_id: UUID | None = None,
) -> FakeParcel:
    return FakeParcel(
        id=id,
        public_id=public_id or uuid4(),
        name=name,
        weight=weight,
        parcel_type_id=parcel_type_id,
        parcel_type=FakeParcelType(name=type_name),
        content_price_usd=content_price_usd,
        delivery_price_rub=delivery_price_rub,
    )
