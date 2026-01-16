from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class ParcelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    weight: float = Field(gt=0)
    parcel_type_id: int = Field(gt=0, le=3)
    content_price_usd: float = Field(ge=0)

class ParcelOut(BaseModel):
    id: int
    public_id: UUID
    name: str
    weight: float
    parcel_type_id: int
    type_name: str
    content_price_usd: float = Field(..., ge=0)
    delivery_price_rub: float | str

class ParcelListOut(BaseModel):
    items: list[ParcelOut]
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=100)
    total: int = Field(..., ge=0)

class ParcelRegisteredOut(BaseModel):
    public_id: UUID
    status: str  # "queued"

class ParcelTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ParcelDetailOut(BaseModel):
    name: str
    weight: float
    parcel_type_id: int
    type_name: str
    content_price_usd: float
    delivery_price_rub: float | str


