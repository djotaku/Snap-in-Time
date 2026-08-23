"""Test culling.py."""

from datetime import datetime, timedelta

from snapintime import culling


def test_retention_cull_keeps_recent_hourly_snapshots():
    now = datetime(2024, 7, 15, 12)
    snapshots = [
        (now - timedelta(hours=hour)).strftime("%Y-%m-%d-%H%M")
        for hour in range(48)
    ]

    assert culling.generate_retention_cull_list(snapshots, now) == []


def test_retention_cull_selects_calendar_representatives():
    now = datetime(2024, 7, 15, 12)
    snapshots = [
        "2024-07-12-0000", "2024-07-12-0600", "2024-07-12-1200", "2024-07-12-1800",
        "2024-07-12-0100", "2024-07-13-0000", "2024-07-13-0600", "2024-07-13-1200",
        "2024-07-13-1800", "2024-07-13-0200", "2024-07-05-1200", "2024-07-05-1800",
        "2024-04-15-1200", "2024-04-15-1800", "2024-01-15-1200", "2024-01-15-1800",
        "not-a-snapshot",
    ]

    culled = culling.generate_retention_cull_list(snapshots, now)

    assert culled == [
        "2024-07-12-0100", "2024-07-13-0200", "2024-07-05-1200",
        "2024-04-15-1200", "2024-01-15-1200",
    ]
    assert "not-a-snapshot" not in culled
