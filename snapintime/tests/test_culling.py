"""Test culling.py."""

from snapintime import culling


def test_cull_hours_24_hours():
    hourly_dir_to_cull = ["2020-03-01-0000", "2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400", "2020-03-01-0500", "2020-03-01-0600", "2020-03-01-0700", "2020-03-01-0800", "2020-03-01-0900", "2020-03-01-1000", "2020-03-01-1100", "2020-03-01-1200", "2020-03-01-1300", "2020-03-01-1400", "2020-03-01-1500", "2020-03-01-1600", "2020-03-01-1700", "2020-03-01-1800", "2020-03-01-1900", "2020-03-01-2000", "2020-03-01-2100", "2020-03-01-2200", "2020-03-01-2300"]
    results = culling.daily_cull(hourly_dir_to_cull)
    assert results == ["2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400", "2020-03-01-0500", "2020-03-01-0700", "2020-03-01-0800", "2020-03-01-0900", "2020-03-01-1000", "2020-03-01-1100", "2020-03-01-1300", "2020-03-01-1400", "2020-03-01-1500", "2020-03-01-1600", "2020-03-01-1700", "2020-03-01-1900", "2020-03-01-2000", "2020-03-01-2100", "2020-03-01-2200", "2020-03-01-2300"]


def test_cull_hours_irregular_hours():
    hourly_dir_to_cull = ["2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400", "2020-03-01-0500", "2020-03-01-0600", "2020-03-01-0700", "2020-03-01-0800", "2020-03-01-1000", "2020-03-01-1100", "2020-03-01-1200", "2020-03-01-1300", "2020-03-01-1400", "2020-03-01-1500", "2020-03-01-1600", "2020-03-01-1700", "2020-03-01-1900", "2020-03-01-2300"]
    results = culling.daily_cull(hourly_dir_to_cull)
    assert results == ["2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400", "2020-03-01-0500", "2020-03-01-0700", "2020-03-01-0800", "2020-03-01-0900", "2020-03-01-1000", "2020-03-01-1100", "2020-03-01-1300", "2020-03-01-1400", "2020-03-01-1500", "2020-03-01-1600", "2020-03-01-1700", "2020-03-01-1900", "2020-03-01-2000", "2020-03-01-2100", "2020-03-01-2200", "2020-03-01-2300"]
