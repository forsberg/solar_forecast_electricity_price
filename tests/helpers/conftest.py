import pytest
import datetime
import zoneinfo

@pytest.fixture
def hourly_forecast():
    return [
        [
            (
                datetime.datetime(
                    2026,
                    1,
                    3,
                    8,
                    44,
                    53,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                0,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 9, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                16,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 10, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                210,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 11, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                358,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 12, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                444,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 13, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                4500,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 14, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                330,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 15, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                175,
            ),
            (
                datetime.datetime(
                    2026,
                    1,
                    3,
                    15,
                    19,
                    4,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                15,
            ),
            (
                datetime.datetime(
                    2026,
                    1,
                    4,
                    8,
                    44,
                    18,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                0,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 9, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                17,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 10, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                215,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 11, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                367,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 12, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                455,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 13, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                448,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 14, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                340,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 15, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                197,
            ),
            (
                datetime.datetime(
                    2026,
                    1,
                    4,
                    15,
                    20,
                    33,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                23,
            ),
        ],
        [
            (
                datetime.datetime(
                    2026,
                    1,
                    3,
                    8,
                    44,
                    53,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                0,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 9, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                36,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 10, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                480,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 11, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                799,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 12, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                943,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 13, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                0,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 14, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                640,
            ),
            (
                datetime.datetime(
                    2026, 1, 3, 15, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                327,
            ),
            (
                datetime.datetime(
                    2026,
                    1,
                    3,
                    15,
                    19,
                    4,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                28,
            ),
            (
                datetime.datetime(
                    2026,
                    1,
                    4,
                    8,
                    44,
                    18,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                0,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 9, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                38,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 10, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                492,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 11, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                819,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 12, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                967,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 13, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                907,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 14, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                658,
            ),
            (
                datetime.datetime(
                    2026, 1, 4, 15, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm")
                ),
                367,
            ),
            (
                datetime.datetime(
                    2026,
                    1,
                    4,
                    15,
                    20,
                    33,
                    tzinfo=zoneinfo.ZoneInfo(key="Europe/Stockholm"),
                ),
                42,
            ),
        ],
    ]

@pytest.fixture
def import_cost_today():
    ret = []
    start_ts = datetime.datetime(2026,1,3,0,0,0,tzinfo=zoneinfo.ZoneInfo('Europe/Stockholm'))
    for i in range(96):
        ret.append({'price':2.0, 'time':(start_ts+datetime.timedelta(minutes=i*15)).isoformat()})
    return ret

@pytest.fixture
def export_income_today():
    ret = []
    start_ts = datetime.datetime(2026,1,3,0,0,0,tzinfo=zoneinfo.ZoneInfo('Europe/Stockholm'))
    for i in range(96):
        ret.append({'price':1.00, 'time':(start_ts+datetime.timedelta(minutes=i*15)).isoformat()})
    return ret

@pytest.fixture
def import_cost_tomorrow():
    ret = []
    start_ts = datetime.datetime(2026,1,4,0,0,0,tzinfo=zoneinfo.ZoneInfo('Europe/Stockholm'))
    for i in range(96):
        ret.append({'price':2.0, 'time':(start_ts+datetime.timedelta(minutes=i*15)).isoformat()})
    return ret

@pytest.fixture
def export_income_tomorrow():
    ret = []
    start_ts = datetime.datetime(2026,1,4,0,0,0,tzinfo=zoneinfo.ZoneInfo('Europe/Stockholm'))
    for i in range(96):
        ret.append({'price':1.00, 'time':(start_ts+datetime.timedelta(minutes=i*15)).isoformat()})
    return ret

