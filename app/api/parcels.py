from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, Query

from app.schemas.parcels import ParcelCreate, ParcelListOut, ParcelRegisteredOut, ParcelTypeOut, ParcelDetailOut
from app.tasks.parcel_registration import register_parcel_task
from app.api.deps import get_session_id, get_parcel_service, get_parcel_type_service
from app.services.parcel_type import ParcelTypeService
from app.services.parcels import ParcelService

router = APIRouter()



@router.get("/parcel-types",response_model=list[ParcelTypeOut])
async def get_parcel_types(service: ParcelTypeService = Depends(get_parcel_type_service)):
    return await service.list_parcel_types()


@router.post("/parcels", response_model=ParcelRegisteredOut, status_code=202)
async def register_parcels(data: ParcelCreate,session_id: str = Depends(get_session_id)):
    public_id = uuid4()

    register_parcel_task.delay(
        payload={
            "public_id": str(public_id),
            "session_id": session_id,
            "name": data.name,
            "weight": data.weight,
            "parcel_type_id": data.parcel_type_id,
            "content_price_usd": data.content_price_usd,
        }
    )

    return {"public_id": public_id, "status": "queued"}



@router.get("/parcels", response_model=ParcelListOut)
async def get_parcels(
    session_id: str = Depends(get_session_id),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type_id: int | None = Query(None, ge=1, le=3),
    has_delivery_cost: bool | None = Query(None),
    service: ParcelService = Depends(get_parcel_service)
):

    return await service.list_parcels(
        session_id=session_id,
        page=page,
        page_size=page_size,
        type_id=type_id,
        has_delivery_cost=has_delivery_cost,
    )


@router.get("/parcels/by_id/{id}", response_model=ParcelDetailOut)
async def get_parcel_by_id(id: int, session_id: str = Depends(get_session_id),
                     service: ParcelService = Depends(get_parcel_service)):

    return await service.get_parcel_by_id(
        parcel_id=id,
        session_id=session_id,
    )


@router.get("/parcels/public/{public_id}", response_model=ParcelDetailOut)
async def get_parcel_by_public_id(public_id: UUID, session_id: str = Depends(get_session_id),
                     service: ParcelService = Depends(get_parcel_service)):

    return await service.get_parcel_by_public_id(
        public_id=public_id,
        session_id=session_id,
    )
