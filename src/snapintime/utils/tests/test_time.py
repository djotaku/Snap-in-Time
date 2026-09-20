from datetime import datetime

import snapintime.utils.date


def test_iso_week():
    assert snapintime.utils.date.iso_week(datetime(2024, 1, 1)) == (2024, 1)


def test_calendar_quarter():
    assert snapintime.utils.date.calendar_quarter(datetime(2024, 7, 1)) == (2024, 3)


def test_quarter_end():
    assert snapintime.utils.date.quarter_end(datetime(2024, 2, 10)) == datetime(2024, 3, 31)
