from datetime import datetime

import snapintime.utils.date


def test_minus_day():
    """Test that the correct date is given when going back one day."""
    today = datetime(year=2020, month=3, day=3)
    new_day = snapintime.utils.date.prior_date(today, 1)
    assert (new_day.year, new_day.month, new_day.day) == (2020, 3, 2)


def test_minus_first_day_of_month():
    """Test that going back back from day 1 of a month will give correct date.

    In this case, going from April 1 back to March 30.
    """
    today = datetime(year=2020, month=4, day=1)
    new_day = snapintime.utils.date.prior_date(today, 1)
    assert (new_day.year, new_day.month, new_day.day) == (2020, 3, 31)


def test_minus_first_day_of_year():
    """Test that going back a day on 1 Jan will go to 31 Dec of prev year."""
    today = datetime(year=2020, month=1, day=1)
    new_day = snapintime.utils.date.prior_date(today, 1)
    assert (new_day.year, new_day.month, new_day.day) == (2019, 12, 31)


def test_3_day_range():
    """Test getting back dates from a 3 day range."""
    today = datetime(year=2020, month=4, day=1)
    day1 = datetime(year=2020, month=3, day=31)
    day2 = datetime(year=2020, month=3, day=30)
    day3 = datetime(year=2020, month=3, day=29)
    date_list = snapintime.utils.date.many_dates(today, 1, 3)
    assert date_list == [day1, day2, day3]