"""Test culling.py."""

import re

from snapintime import culling


def test_split_dir_hours():
    list = ["match", "not me", "another match"]
    reg_ex = re.compile('match')
    result = culling.split_dir_hours(list, reg_ex)
    assert result == ["match", "another match"]


def test_cull_hours_24_hours():
    """Test the daily cull with a perfect list in which there are hourly snapshots for an entire day."""
    hourly_dir_to_cull = ["2020-03-01-0000", "2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300",
                          "2020-03-01-0400", "2020-03-01-0500", "2020-03-01-0600", "2020-03-01-0700",
                          "2020-03-01-0800", "2020-03-01-0900", "2020-03-01-1000", "2020-03-01-1100",
                          "2020-03-01-1200", "2020-03-01-1300", "2020-03-01-1400", "2020-03-01-1500",
                          "2020-03-01-1600", "2020-03-01-1700", "2020-03-01-1800", "2020-03-01-1900",
                          "2020-03-01-2000", "2020-03-01-2100", "2020-03-01-2200", "2020-03-01-2300"]
    results = culling.daily_cull(hourly_dir_to_cull)
    assert results == ["2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400",
                       "2020-03-01-0500", "2020-03-01-0700", "2020-03-01-0800", "2020-03-01-0900",
                       "2020-03-01-1000", "2020-03-01-1100", "2020-03-01-1300", "2020-03-01-1400",
                       "2020-03-01-1500", "2020-03-01-1600", "2020-03-01-1700", "2020-03-01-1900",
                       "2020-03-01-2000", "2020-03-01-2100", "2020-03-01-2200", "2020-03-01-2300"]


def test_cull_hours_irregular_hours():
    """Test the daily cull if there aren't 24, perfect hourly snapshots."""
    hourly_dir_to_cull = ["2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400",
                          "2020-03-01-0500", "2020-03-01-0600", "2020-03-01-0700", "2020-03-01-0800",
                          "2020-03-01-1000", "2020-03-01-1100", "2020-03-01-1200", "2020-03-01-1300",
                          "2020-03-01-1400", "2020-03-01-1500", "2020-03-01-1600", "2020-03-01-1700",
                          "2020-03-01-1900", "2020-03-01-2300"]
    results = culling.daily_cull(hourly_dir_to_cull)
    assert results == ["2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400", "2020-03-01-0500",
                       "2020-03-01-0700", "2020-03-01-0800", "2020-03-01-1000", "2020-03-01-1100",
                       "2020-03-01-1300", "2020-03-01-1400", "2020-03-01-1500", "2020-03-01-1600",
                       "2020-03-01-1700", "2020-03-01-2300"]


def test_cull_hours_only_one_entry():
    """Test the daily cull if there is only one entry."""
    hourly_dir_to_cull = ["2020-03-01-0100"]
    results = culling.daily_cull(hourly_dir_to_cull)
    assert results == []


def test_cull_hours_no_entries():
    """Test the daily cull if there are no snapshots to cull."""
    hourly_dir_to_cull = []
    results = culling.daily_cull(hourly_dir_to_cull)
    assert results == []


def test_weekly_cull_perfect_list():
    """Test weekly cull if there are 4 snapshots to cull."""
    weekly_dir_to_cull = ["2020-03-16-0000", "2020-03-16-0600", "2020-03-16-1200", "2020-03-16-1800"]
    results = culling.weekly_cull(weekly_dir_to_cull)
    assert results == ["2020-03-16-0000", "2020-03-16-0600", "2020-03-16-1200"]


def test_weekly_cull_no_entries():
    """Test the weekly cull if there are no snapshots to cull."""
    weekly_dir_to_cull = []
    results = culling.weekly_cull(weekly_dir_to_cull)
    assert results == []
