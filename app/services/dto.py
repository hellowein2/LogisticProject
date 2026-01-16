from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ParcelRegistrationDTO:
    public_id: UUID
    session_id: str
    name: str
    weight: float
    parcel_type_id: int
    content_price_usd: float