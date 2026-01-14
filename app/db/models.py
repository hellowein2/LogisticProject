from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid

class ParcelType(Base):
    __tablename__ = "parcel_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


    parcels = relationship("Parcel", back_populates="parcel_type")


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True)
    public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    session_id = Column(String(36), index=True, nullable=False)
    name = Column(String(100), nullable=False)
    weight = Column(Float, nullable=False)
    content_price_usd = Column(Float, nullable=False)
    delivery_price_rub = Column(Float, nullable=True, index=True)
    parcel_type_id = Column(Integer, ForeignKey("parcel_types.id"), nullable=False)

    parcel_type = relationship("ParcelType", back_populates="parcels")