from uuid import UUID

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.services.parcel_registration import ParcelRegistrationService
from app.services.dto import ParcelRegistrationDTO
from app.exceptions.parcels import ParcelAlreadyExistsError, InvalidParcelTypeError
from loguru import logger

@celery_app.task(
    name="app.tasks.parcels.register_parcel",
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def register_parcel_task(self, *, payload: dict) -> dict:
    logger.info(
        "Register parcel task started",
        task_id=self.request.id,
        public_id=payload.get("public_id"),
    )

    dto = ParcelRegistrationDTO(
        public_id=UUID(payload["public_id"]),
        session_id=str(payload["session_id"]),
        name=str(payload["name"]),
        weight=float(payload["weight"]),
        parcel_type_id=int(payload["parcel_type_id"]),
        content_price_usd=float(payload["content_price_usd"]),
    )

    db = SessionLocal()
    try:
        service = ParcelRegistrationService(db)

        logger.info(
            "Parcel registered successfully",
            task_id=self.request.id,
            public_id=str(dto.public_id),
        )

        return service.register(dto)

    except ParcelAlreadyExistsError:
        logger.info(
            "Parcel already exists",
            task_id=self.request.id,
            public_id=str(dto.public_id),
        )
        return {"status": "already_exists", "public_id": str(dto.public_id)}

    except InvalidParcelTypeError as e:
        logger.warning(
            "Invalid parcel type",
            task_id=self.request.id,
            parcel_type_id=e.parcel_type_id,
            public_id=str(dto.public_id),
        )

        return {
            "status": "invalid_parcel_type",
            "parcel_type_id": e.parcel_type_id,
            "public_id": str(dto.public_id),
        }

    except Exception:
        logger.exception(
            "Unexpected error while registering parcel",
            task_id=self.request.id,
            public_id=payload.get("public_id"),
        )
        raise

    finally:
        db.close()

