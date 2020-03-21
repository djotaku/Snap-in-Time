"""Provide date and Time Operations needed by snapintime."""

from datetime import datetime, timedelta


def prior_date(start_date: datetime, day: int = 0) -> datetime:
    """Provide a prior date offset by the variable given in day.

    Unintuitively, positive numbers subtract days.

    :param start_date: The date from which you want to count back or forward.
    :param day: The number of days you want to go back.
    :returns: A datetime object day amount of days in the past.
    """
    delta_days = timedelta(days=day)
    prev_date: datetime = start_date - delta_days
    return prev_date


def many_dates(start_date: datetime, interval_start: int, interval_end: int) -> list:
    """Provide a list of dates within a certain range.

    Used by quarterly culling and yearly culling to determine date range to cull.

    :param start_date: The reference point for the intervals
    :param interval_start: How many days ago you want to start getting dates from.
    :param interval_end: How many days ago you want to stop getting dates from.
    """
    return_list = []
    for day in range(interval_start, interval_end+1):
        return_list.append(prior_date(start_date, day))
    return return_list


def quarterly_weeks(start_date: datetime) -> list:
    """Provide a list of 13 weekly date lists.

    :param start_date: Date from which to go back a quarter.
    :returns: A list of lists containing datetime objects.
    """
    list_of_weeks = []
    for number in range(0, 90, 7):
        list_of_weeks.append(many_dates(start_date, 90+number, 96+number))
    return list_of_weeks
