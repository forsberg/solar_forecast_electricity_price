import logging
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from collections import defaultdict
from dataclasses import dataclass

_LOGGER = logging.getLogger(__name__)


@dataclass
class PriceInfo:
    prices_today: list
    prices_tomorrow: list
    price_now: float


def calculate_prices(
    forecasts: list[list[tuple[str, int]]],
    now: datetime,
    import_cost_today: list[dict[str, str | float]],
    export_income_today: list[dict[str, str | float]],
    import_cost_tomorrow: list[dict[str, str | float]],
    export_income_tomorrow: list[dict[str, str | float]],
    power_draw: int,
):
    # Expected input for forecasts is a list of lists where the inner list looks something like this:
    # [('2026-01-03T07:44:53+00:00', 0),
    #  ('2026-01-03T08:00:00+00:00', 16),
    #  ('2026-01-03T09:00:00+00:00', 210),
    #  ('2026-01-03T10:00:00+00:00', 358),
    #  ('2026-01-03T11:00:00+00:00', 444),
    #  ('2026-01-03T12:00:00+00:00', 436),
    #  ('2026-01-03T13:00:00+00:00', 330),
    #  ('2026-01-03T14:00:00+00:00', 175),
    #  ('2026-01-03T14:19:04+00:00', 15),
    #  ('2026-01-04T07:44:18+00:00', 0),
    #  ('2026-01-04T08:00:00+00:00', 17),
    #  ('2026-01-04T09:00:00+00:00', 215),
    #  ('2026-01-04T10:00:00+00:00', 367),
    #  ('2026-01-04T11:00:00+00:00', 455),
    #  ('2026-01-04T12:00:00+00:00', 448),
    #  ('2026-01-04T13:00:00+00:00', 340),
    #  ('2026-01-04T14:00:00+00:00', 197),
    #  ('2026-01-04T14:20:33+00:00', 23)]
    # I.e (timestamp, Wh), where Wh is the amount of energy
    # expected for the timeperiod between the previous timestamp and
    # the timestamp on the row. I.e, the first entry seems to be
    # sunrise, showing the production since the last entry of the night
    # before (0), and the last entry is sunset.

    # We assume the data is in the format received from API call to
    # forecast.solar, as described in their documentation:
    # https://doc.forecast.solar/doku.php?id=api:estimate

    first_forecast = forecasts[0]

    # Figure out the forecast precision, as it depends on your subscription model for forecast.solar
    # I.e the free version will have one per hour, with paid subscriptions giving you a more detailed result
    timedelta_between_day_entries = first_forecast[2][0] - first_forecast[1][0]

    if len(import_cost_today) == 24:
        output_precision = timedelta(hours=1)
    elif len(import_cost_today) == 96:
        output_precision = timedelta(minutes=15)

    combined_solar_forecast = defaultdict(lambda: 0)

    for forecast in forecasts:
        for idx in range(len(forecast) - 1):
            (ts, wh) = forecast[idx]
            (next_ts, next_wh) = forecast[idx + 1]
            delta = next_ts - ts

            if next_wh == 0:
                continue

            if delta <= timedelta(minutes=15):
                combined_solar_forecast[next_ts - timedelta(minutes=15)] += next_wh
            elif delta > timedelta(minutes=15) and delta <= timedelta(minutes=30):
                combined_solar_forecast[next_ts - timedelta(minutes=30)] += next_wh / 2
                combined_solar_forecast[next_ts - timedelta(minutes=15)] += next_wh / 2
            elif delta > timedelta(minutes=30) and delta <= timedelta(minutes=45):
                combined_solar_forecast[next_ts - timedelta(minutes=45)] += next_wh / 3
                combined_solar_forecast[next_ts - timedelta(minutes=30)] += next_wh / 3
                combined_solar_forecast[next_ts - timedelta(minutes=15)] += next_wh / 3
            else:
                combined_solar_forecast[next_ts - timedelta(minutes=60)] += next_wh / 4
                combined_solar_forecast[next_ts - timedelta(minutes=45)] += next_wh / 4
                combined_solar_forecast[next_ts - timedelta(minutes=30)] += next_wh / 4
                combined_solar_forecast[next_ts - timedelta(minutes=15)] += next_wh / 4

    current: float | None = None

    def _combine_prices(import_cost, export_income):
        ret = []
        for idx in range(len(import_cost)):
            import_cost_entry = import_cost[idx]
            export_income_entry = export_income[idx]
            start_ts = datetime.fromisoformat(import_cost_entry["time"])

            solar_share = 0.0
            if start_ts in combined_solar_forecast:
                solar_share = min(1.0, combined_solar_forecast[start_ts] / (power_draw / 4)) # FIXME: 15m assumption

            cost = round(
                solar_share * export_income_entry["price"]
                + (1.0 - solar_share) * import_cost_entry["price"],
                4,
            )

            if start_ts in combined_solar_forecast and _LOGGER.isEnabledFor(logging.DEBUG):
                _LOGGER.debug(
                    f"{start_ts} - solar share is {solar_share}, cost is {cost}, Wh this period: {combined_solar_forecast[start_ts]}"
                )

            ret.append(
                {
                    "time": start_ts,
                    "price": cost,
                }
            )

            nonlocal current
            if start_ts <= now < (start_ts + output_precision):
                current = cost

        return ret

    today = _combine_prices(import_cost_today, export_income_today)
    tomorrow = _combine_prices(import_cost_tomorrow, export_income_tomorrow)

    return PriceInfo(today, tomorrow, current)
