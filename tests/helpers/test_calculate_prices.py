from datetime import datetime
from zoneinfo import ZoneInfo
from custom_components.actual_price_with_solar.helpers.calculate_prices import (
    calculate_prices,
)
import pytest


def test_hourly_forecast_15m_prices(
    hourly_forecast,
    import_cost_today,
    export_income_today,
    import_cost_tomorrow,
    export_income_tomorrow,
):
    result = calculate_prices(
        hourly_forecast,
        datetime(2026, 1, 3, 13, 2, tzinfo=ZoneInfo("Europe/Stockholm")),
        import_cost_today,
        export_income_today,
        import_cost_tomorrow,
        export_income_tomorrow,
        4500,
    )

    assert len(result.prices_today) == 96
    assert len(result.prices_tomorrow) == 96
    assert result.prices_today[0]['price'] == pytest.approx(2.0)
    assert result.prices_today[12*4]['time'] == datetime(2026,1,3,12,0,tzinfo=ZoneInfo("Europe/Stockholm"))
    # At 12:00 the available solar power is exactly 4500W, covering the entire power draw from charging.
    assert result.prices_today[12*4]['price'] == pytest.approx(1.0)


