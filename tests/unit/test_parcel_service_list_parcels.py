import pytest
from dataclasses import dataclass
from unittest.mock import AsyncMock

from app.services.parcels import ParcelService
from tests.fakes.parcels import parcel_factory


@dataclass(frozen=True, slots=True)
class ListParcelsCase:
    query_args: dict
    repo_items: list
    repo_total: int
    expected_delivery_values: list


CASES = [
    ListParcelsCase(
        query_args=dict(session_id="sid-1", page=1, page_size=10, type_id=None, has_delivery_cost=None),
        repo_items=[parcel_factory(id=1, delivery_price_rub=1500), parcel_factory(id=2, delivery_price_rub=None)],
        repo_total=2,
        expected_delivery_values=[1500, "Не рассчитано"],
    ),
    ListParcelsCase(
        query_args=dict(session_id="sid-2", page=2, page_size=5, type_id=1, has_delivery_cost=True),
        repo_items=[parcel_factory(id=10, type_name="clothes", delivery_price_rub=999)],
        repo_total=1,
        expected_delivery_values=[999],
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("case", CASES, ids=["no_filters", "filtered_has_cost"])
async def test_list_parcels_contract_and_mapping(case: ListParcelsCase):
    repo = AsyncMock()
    repo.list_by_session.return_value = (case.repo_items, case.repo_total)

    service = ParcelService(repo)
    result = await service.list_parcels(**case.query_args)

    repo.list_by_session.assert_awaited_once_with(**case.query_args)

    assert result.page == case.query_args["page"]
    assert result.page_size == case.query_args["page_size"]
    assert result.total == case.repo_total
    assert len(result.items) == len(case.repo_items)

    for dto, model, expected_delivery in zip(result.items, case.repo_items, case.expected_delivery_values, strict=True):
        assert dto.id == model.id
        assert dto.public_id == model.public_id
        assert dto.name == model.name
        assert dto.weight == float(model.weight)
        assert dto.parcel_type_id == model.parcel_type_id
        assert dto.type_name == model.parcel_type.name
        assert dto.content_price_usd == float(model.content_price_usd)
        assert dto.delivery_price_rub == expected_delivery
