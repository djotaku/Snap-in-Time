"""Provide date and Time Operations needed by snapintime."""

from datetime import datetime, timedelta


def prior_date(startdate: datetime, day: int = 0) -> datetime:
    """Provide a prior date offset by the variable given in day.

    Unintuitively, positive numbers subtract days.

    :param startdate: The date from which you want to count back or forward.
    :param day: The number of days you want to go back.
    """
    delta_days = timedelta(days=day)
    prev_date = startdate - delta_days
    return prev_date
