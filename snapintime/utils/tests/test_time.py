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


def test_quarterly_weeks():
    """Test that the right dates are grabbed."""
    today = datetime(year=2020, month=7, day=1)
    week1 = [datetime(year=2020, month=4, day=2), datetime(year=2020, month=4, day=1),
             datetime(year=2020, month=3, day=31), datetime(year=2020, month=3, day=30),
             datetime(year=2020, month=3, day=29), datetime(year=2020, month=3, day=28),
             datetime(year=2020, month=3, day=27)]
    week2 = [datetime(year=2020, month=3, day=26), datetime(year=2020, month=3, day=25),
             datetime(year=2020, month=3, day=24), datetime(year=2020, month=3, day=23),
             datetime(year=2020, month=3, day=22), datetime(year=2020, month=3, day=21),
             datetime(year=2020, month=3, day=20)]
    week3 = [datetime(year=2020, month=3, day=19), datetime(year=2020, month=3, day=18),
             datetime(year=2020, month=3, day=17), datetime(year=2020, month=3, day=16),
             datetime(year=2020, month=3, day=15), datetime(year=2020, month=3, day=14),
             datetime(year=2020, month=3, day=13)]
    week4 = [datetime(year=2020, month=3, day=12), datetime(year=2020, month=3, day=11),
             datetime(year=2020, month=3, day=10), datetime(year=2020, month=3, day=9),
             datetime(year=2020, month=3, day=8), datetime(year=2020, month=3, day=7),
             datetime(year=2020, month=3, day=6)]
    week5 = [datetime(year=2020, month=3, day=5), datetime(year=2020, month=3, day=4),
             datetime(year=2020, month=3, day=3), datetime(year=2020, month=3, day=2),
             datetime(year=2020, month=3, day=1), datetime(year=2020, month=2, day=29),
             datetime(year=2020, month=2, day=28)]
    week6 = [datetime(year=2020, month=2, day=27), datetime(year=2020, month=2, day=26),
             datetime(year=2020, month=2, day=25), datetime(year=2020, month=2, day=24),
             datetime(year=2020, month=2, day=23), datetime(year=2020, month=2, day=22),
             datetime(year=2020, month=2, day=21)]
    week7 = [datetime(year=2020, month=2, day=20), datetime(year=2020, month=2, day=19),
             datetime(year=2020, month=2, day=18), datetime(year=2020, month=2, day=17),
             datetime(year=2020, month=2, day=16), datetime(year=2020, month=2, day=15),
             datetime(year=2020, month=2, day=14)]
    week8 = [datetime(year=2020, month=2, day=13), datetime(year=2020, month=2, day=12),
             datetime(year=2020, month=2, day=11), datetime(year=2020, month=2, day=10),
             datetime(year=2020, month=2, day=9), datetime(year=2020, month=2, day=8),
             datetime(year=2020, month=2, day=7)]
    week9 = [datetime(year=2020, month=2, day=6), datetime(year=2020, month=2, day=5),
             datetime(year=2020, month=2, day=4), datetime(year=2020, month=2, day=3),
             datetime(year=2020, month=2, day=2), datetime(year=2020, month=2, day=1),
             datetime(year=2020, month=1, day=31)]
    week10 = [datetime(year=2020, month=1, day=30), datetime(year=2020, month=1, day=29),
              datetime(year=2020, month=1, day=28), datetime(year=2020, month=1, day=27),
              datetime(year=2020, month=1, day=26), datetime(year=2020, month=1, day=25),
              datetime(year=2020, month=1, day=24)]
    week11 = [datetime(year=2020, month=1, day=23), datetime(year=2020, month=1, day=22),
              datetime(year=2020, month=1, day=21), datetime(year=2020, month=1, day=20),
              datetime(year=2020, month=1, day=19), datetime(year=2020, month=1, day=18),
              datetime(year=2020, month=1, day=17)]
    week12 = [datetime(year=2020, month=1, day=16), datetime(year=2020, month=1, day=15),
              datetime(year=2020, month=1, day=14), datetime(year=2020, month=1, day=13),
              datetime(year=2020, month=1, day=12), datetime(year=2020, month=1, day=11),
              datetime(year=2020, month=1, day=10)]
    week13 = [datetime(year=2020, month=1, day=9), datetime(year=2020, month=1, day=8),
              datetime(year=2020, month=1, day=7), datetime(year=2020, month=1, day=6),
              datetime(year=2020, month=1, day=5), datetime(year=2020, month=1, day=4),
              datetime(year=2020, month=1, day=3)]
    list_of_weeks = snapintime.utils.date.quarterly_weeks(today)
    assert list_of_weeks == [week1, week2, week3, week4, week5, week6, week7, week8, week9, week10, week11, week12,
                             week13]
