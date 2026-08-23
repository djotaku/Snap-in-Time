"""Provide date and Time Operations needed by snapintime."""

import calendar
from datetime import datetime


def iso_week(start_date: datetime) -> tuple[int, int]:
    """Return the ISO calendar year and week containing ``start_date``."""
    iso_date = start_date.isocalendar()
    return iso_date.year, iso_date.week


def calendar_quarter(start_date: datetime) -> tuple[int, int]:
    """Return the calendar year and quarter containing ``start_date``."""
    return start_date.year, (start_date.month - 1) // 3 + 1


def quarter_end(start_date: datetime) -> datetime:
    """Return the final day of ``start_date``'s calendar quarter."""
    quarter = (start_date.month - 1) // 3
    end_month = quarter * 3 + 3
    end_day = calendar.monthrange(start_date.year, end_month)[1]
    return start_date.replace(month=end_month, day=end_day)
