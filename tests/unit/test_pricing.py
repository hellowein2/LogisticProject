import pytest
from app.services.parcel_registration import _calc_delivery_price_rub


@pytest.mark.parametrize(
    "weight, content_price_usd, usd_to_rub, expected",
    [
        (10.0, 200.0, 75.0, round((10 * 0.5 + 200 * 0.01) * 75)),
        (1.0, 100.0, 90.0, round((1 * 0.5 + 100 * 0.01) * 90)),
        (5.5, 0.0, 80.0, round((5.5 * 0.5) * 80)),
        (0.0, 50.0, 70.0, round((50 * 0.01) * 70)),
    ],
)
def test_calc_delivery_price_rub(weight, content_price_usd, usd_to_rub, expected):
    result = _calc_delivery_price_rub(weight, content_price_usd, usd_to_rub)
    assert result == expected


@pytest.mark.parametrize(
    "weight, content_price_usd, usd_to_rub",
    [
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 90.0),
        (0.0, 100.0, 0.0),
    ],
)
def test_calc_delivery_price_rub_zero_cases(weight, content_price_usd, usd_to_rub):
    result = _calc_delivery_price_rub(weight, content_price_usd, usd_to_rub)
    assert result == 0