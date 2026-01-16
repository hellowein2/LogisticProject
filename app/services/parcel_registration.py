from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.repositories.parcels import SyncParcelRepository
from app.repositories.parcel_type import SyncParcelTypeRepository
from app.services.rates import get_usd_rub_rate_cached
from app.services.rates import get_redis_client
from app.services.dto import ParcelRegistrationDTO
from app.exceptions.parcels import InvalidParcelTypeError, ParcelAlreadyExistsError

from loguru import logger



def _sqlstate_from_integrity_error(e: IntegrityError) -> str | None:
    return getattr(getattr(e, "orig", None), "sqlstate", None)

def _calc_delivery_price_rub(weight: float, content_price_usd: float, usd_to_rub: float) -> float:
    return round((weight * 0.5 + content_price_usd * 0.01) * usd_to_rub)



class ParcelRegistrationService:
    def __init__(self, db: Session):
        self.db = db
        self.parcels = SyncParcelRepository(db)
        self.parcel_types = SyncParcelTypeRepository(db)

    def register(self, dto: ParcelRegistrationDTO) -> dict:
        log = logger.bind(sid=dto.session_id, public_id=str(dto.public_id))

        type_id = int(dto.parcel_type_id)
        if not self.parcel_types.parcel_type_exists(type_id):
            log.info("Invalid parcel type")
            raise InvalidParcelTypeError(type_id)

        r = get_redis_client()
        usd_to_rub = get_usd_rub_rate_cached(r)
        delivery_price = _calc_delivery_price_rub(
            weight=float(dto.weight),
            content_price_usd=float(dto.content_price_usd),
            usd_to_rub=float(usd_to_rub)
        )

        try:
            self.parcels.create(
                public_id=dto.public_id,
                session_id=dto.session_id,
                name=dto.name,
                weight=float(dto.weight),
                parcel_type_id=int(dto.parcel_type_id),
                content_price_usd=float(dto.content_price_usd),
                delivery_price_rub=float(delivery_price),
            )
            self.db.commit()

            log.info("Parcel registered")
            return {"status": "created", "public_id": str(dto.public_id)}
        except IntegrityError as e:
            self.db.rollback()
            sqlstate = _sqlstate_from_integrity_error(e)
            if sqlstate == "23505":
                log.info("Parcel already exists")
                raise ParcelAlreadyExistsError() from e

            log.exception("Integrity error while registering parcel")
            raise

        except Exception:
            self.db.rollback()
            log.exception("Unexpected error while registering parcel")
            raise



