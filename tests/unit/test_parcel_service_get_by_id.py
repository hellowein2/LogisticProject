import pytest
from unittest.mock import AsyncMock

from app.services.parcels import ParcelService
from app.exceptions.parcels import ParcelNotFoundError

from tests.fakes.parcels import parcel_factory


@pytest.mark.asyncio
async def test_get_parcel_by_id_returns_detail_dto_and_maps_fields():
    repo = AsyncMock()


    model = parcel_factory(id=123, type_name="clothes", delivery_price_rub=None)
    repo.get_by_id_for_session.return_value = model

    service = ParcelService(repo)

    dto = await service.get_parcel_by_id(parcel_id=123, session_id="sid-1")

    repo.get_by_id_for_session.assert_awaited_once_with(
        parcel_id=123,
        session_id="sid-1",
    )

    assert dto.name == model.name
    assert dto.weight == float(model.weight)
    assert dto.parcel_type_id == model.parcel_type_id
    assert dto.type_name == model.parcel_type.name
    assert dto.content_price_usd == float(model.content_price_usd)
    assert dto.delivery_price_rub == "Не рассчитано"





@pytest.mark.asyncio
async def test_get_parcel_by_id_raises_if_not_found():
    repo = AsyncMock()
    repo.get_by_id_for_session.return_value = None

    service = ParcelService(repo)

    with pytest.raises(ParcelNotFoundError):
        await service.get_parcel_by_id(parcel_id=123, session_id="sid-1")

    repo.get_by_id_for_session.assert_awaited_once_with(
        parcel_id=123,
        session_id="sid-1",
    )
import pytest
from unittest.mock import AsyncMock

from app.services.parcels import ParcelService
from app.exceptions.parcels import ParcelNotFoundError

from tests.fakes.parcels import parcel_factory


@pytest.mark.asyncio
async def test_get_parcel_by_id_returns_detail_dto_and_maps_fields():
    repo = AsyncMock()


    model = parcel_factory(id=123, type_name="clothes", delivery_price_rub=None)
    repo.get_by_id_for_session.return_value = model

    service = ParcelService(repo)

    dto = await service.get_parcel_by_id(parcel_id=123, session_id="sid-1")

    repo.get_by_id_for_session.assert_awaited_once_with(
        parcel_id=123,
        session_id="sid-1",
    )

    assert dto.name == model.name
    assert dto.weight == float(model.weight)
    assert dto.parcel_type_id == model.parcel_type_id
    assert dto.type_name == model.parcel_type.name
    assert dto.content_price_usd == float(model.content_price_usd)
    assert dto.delivery_price_rub == "Не рассчитано"





@pytest.mark.asyncio
async def test_get_parcel_by_id_raises_if_not_found():
    repo = AsyncMock()
    repo.get_by_id_for_session.return_value = None

    service = ParcelService(repo)

    with pytest.raises(ParcelNotFoundError):
        await service.get_parcel_by_id(parcel_id=123, session_id="sid-1")

    repo.get_by_id_for_session.assert_awaited_once_with(
        parcel_id=123,
        session_id="sid-1",
    )
