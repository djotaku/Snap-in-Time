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


def test_yearly_quarters():
    """Test that the right dates are grabbed."""
    today = datetime(year=2020, month=3, day=28)
    list_of_quarters = snapintime.utils.date.yearly_quarters(today)
    quarter1 = [datetime(2019, 3, 29, 0, 0), datetime(2019, 3, 28, 0, 0), datetime(2019, 3, 27, 0, 0),
                datetime(2019, 3, 26, 0, 0), datetime(2019, 3, 25, 0, 0), datetime(2019, 3, 24, 0, 0),
                datetime(2019, 3, 23, 0, 0), datetime(2019, 3, 22, 0, 0), datetime(2019, 3, 21, 0, 0),
                datetime(2019, 3, 20, 0, 0), datetime(2019, 3, 19, 0, 0), datetime(2019, 3, 18, 0, 0),
                datetime(2019, 3, 17, 0, 0), datetime(2019, 3, 16, 0, 0), datetime(2019, 3, 15, 0, 0),
                datetime(2019, 3, 14, 0, 0), datetime(2019, 3, 13, 0, 0), datetime(2019, 3, 12, 0, 0),
                datetime(2019, 3, 11, 0, 0), datetime(2019, 3, 10, 0, 0), datetime(2019, 3, 9, 0, 0),
                datetime(2019, 3, 8, 0, 0), datetime(2019, 3, 7, 0, 0), datetime(2019, 3, 6, 0, 0),
                datetime(2019, 3, 5, 0, 0), datetime(2019, 3, 4, 0, 0), datetime(2019, 3, 3, 0, 0),
                datetime(2019, 3, 2, 0, 0), datetime(2019, 3, 1, 0, 0), datetime(2019, 2, 28, 0, 0),
                datetime(2019, 2, 27, 0, 0), datetime(2019, 2, 26, 0, 0), datetime(2019, 2, 25, 0, 0),
                datetime(2019, 2, 24, 0, 0), datetime(2019, 2, 23, 0, 0), datetime(2019, 2, 22, 0, 0),
                datetime(2019, 2, 21, 0, 0), datetime(2019, 2, 20, 0, 0), datetime(2019, 2, 19, 0, 0),
                datetime(2019, 2, 18, 0, 0), datetime(2019, 2, 17, 0, 0), datetime(2019, 2, 16, 0, 0),
                datetime(2019, 2, 15, 0, 0), datetime(2019, 2, 14, 0, 0), datetime(2019, 2, 13, 0, 0),
                datetime(2019, 2, 12, 0, 0), datetime(2019, 2, 11, 0, 0), datetime(2019, 2, 10, 0, 0),
                datetime(2019, 2, 9, 0, 0), datetime(2019, 2, 8, 0, 0), datetime(2019, 2, 7, 0, 0),
                datetime(2019, 2, 6, 0, 0), datetime(2019, 2, 5, 0, 0), datetime(2019, 2, 4, 0, 0),
                datetime(2019, 2, 3, 0, 0), datetime(2019, 2, 2, 0, 0), datetime(2019, 2, 1, 0, 0),
                datetime(2019, 1, 31, 0, 0), datetime(2019, 1, 30, 0, 0), datetime(2019, 1, 29, 0, 0),
                datetime(2019, 1, 28, 0, 0), datetime(2019, 1, 27, 0, 0), datetime(2019, 1, 26, 0, 0),
                datetime(2019, 1, 25, 0, 0), datetime(2019, 1, 24, 0, 0), datetime(2019, 1, 23, 0, 0),
                datetime(2019, 1, 22, 0, 0), datetime(2019, 1, 21, 0, 0), datetime(2019, 1, 20, 0, 0),
                datetime(2019, 1, 19, 0, 0), datetime(2019, 1, 18, 0, 0), datetime(2019, 1, 17, 0, 0),
                datetime(2019, 1, 16, 0, 0), datetime(2019, 1, 15, 0, 0), datetime(2019, 1, 14, 0, 0),
                datetime(2019, 1, 13, 0, 0), datetime(2019, 1, 12, 0, 0), datetime(2019, 1, 11, 0, 0),
                datetime(2019, 1, 10, 0, 0), datetime(2019, 1, 9, 0, 0), datetime(2019, 1, 8, 0, 0),
                datetime(2019, 1, 7, 0, 0), datetime(2019, 1, 6, 0, 0), datetime(2019, 1, 5, 0, 0),
                datetime(2019, 1, 4, 0, 0), datetime(2019, 1, 3, 0, 0), datetime(2019, 1, 2, 0, 0),
                datetime(2019, 1, 1, 0, 0), datetime(2018, 12, 31, 0, 0), datetime(2018, 12, 30, 0, 0),
                datetime(2018, 12, 29, 0, 0)]
    quarter2 = [datetime(2018, 12, 28, 0, 0), datetime(2018, 12, 27, 0, 0),
                datetime(2018, 12, 26, 0, 0), datetime(2018, 12, 25, 0, 0), datetime(2018, 12, 24, 0, 0),
                datetime(2018, 12, 23, 0, 0), datetime(2018, 12, 22, 0, 0), datetime(2018, 12, 21, 0, 0),
                datetime(2018, 12, 20, 0, 0), datetime(2018, 12, 19, 0, 0), datetime(2018, 12, 18, 0, 0),
                datetime(2018, 12, 17, 0, 0), datetime(2018, 12, 16, 0, 0), datetime(2018, 12, 15, 0, 0),
                datetime(2018, 12, 14, 0, 0), datetime(2018, 12, 13, 0, 0), datetime(2018, 12, 12, 0, 0),
                datetime(2018, 12, 11, 0, 0), datetime(2018, 12, 10, 0, 0), datetime(2018, 12, 9, 0, 0),
                datetime(2018, 12, 8, 0, 0), datetime(2018, 12, 7, 0, 0), datetime(2018, 12, 6, 0, 0),
                datetime(2018, 12, 5, 0, 0), datetime(2018, 12, 4, 0, 0), datetime(2018, 12, 3, 0, 0),
                datetime(2018, 12, 2, 0, 0), datetime(2018, 12, 1, 0, 0), datetime(2018, 11, 30, 0, 0),
                datetime(2018, 11, 29, 0, 0), datetime(2018, 11, 28, 0, 0), datetime(2018, 11, 27, 0, 0),
                datetime(2018, 11, 26, 0, 0), datetime(2018, 11, 25, 0, 0), datetime(2018, 11, 24, 0, 0),
                datetime(2018, 11, 23, 0, 0), datetime(2018, 11, 22, 0, 0), datetime(2018, 11, 21, 0, 0),
                datetime(2018, 11, 20, 0, 0), datetime(2018, 11, 19, 0, 0), datetime(2018, 11, 18, 0, 0),
                datetime(2018, 11, 17, 0, 0), datetime(2018, 11, 16, 0, 0), datetime(2018, 11, 15, 0, 0),
                datetime(2018, 11, 14, 0, 0), datetime(2018, 11, 13, 0, 0), datetime(2018, 11, 12, 0, 0),
                datetime(2018, 11, 11, 0, 0), datetime(2018, 11, 10, 0, 0), datetime(2018, 11, 9, 0, 0),
                datetime(2018, 11, 8, 0, 0), datetime(2018, 11, 7, 0, 0), datetime(2018, 11, 6, 0, 0),
                datetime(2018, 11, 5, 0, 0), datetime(2018, 11, 4, 0, 0), datetime(2018, 11, 3, 0, 0),
                datetime(2018, 11, 2, 0, 0), datetime(2018, 11, 1, 0, 0), datetime(2018, 10, 31, 0, 0),
                datetime(2018, 10, 30, 0, 0), datetime(2018, 10, 29, 0, 0), datetime(2018, 10, 28, 0, 0),
                datetime(2018, 10, 27, 0, 0), datetime(2018, 10, 26, 0, 0), datetime(2018, 10, 25, 0, 0),
                datetime(2018, 10, 24, 0, 0), datetime(2018, 10, 23, 0, 0), datetime(2018, 10, 22, 0, 0),
                datetime(2018, 10, 21, 0, 0), datetime(2018, 10, 20, 0, 0), datetime(2018, 10, 19, 0, 0),
                datetime(2018, 10, 18, 0, 0), datetime(2018, 10, 17, 0, 0),datetime(2018, 10, 16, 0, 0),
                datetime(2018, 10, 15, 0, 0), datetime(2018, 10, 14, 0, 0), datetime(2018, 10, 13, 0, 0),
                datetime(2018, 10, 12, 0, 0), datetime(2018, 10, 11, 0, 0), datetime(2018, 10, 10, 0, 0),
                datetime(2018, 10, 9, 0, 0), datetime(2018, 10, 8, 0, 0), datetime(2018, 10, 7, 0, 0),
                datetime(2018, 10, 6, 0, 0), datetime(2018, 10, 5, 0, 0), datetime(2018, 10, 4, 0, 0),
                datetime(2018, 10, 3, 0, 0), datetime(2018, 10, 2, 0, 0), datetime(2018, 10, 1, 0, 0),
                datetime(2018, 9, 30, 0, 0), datetime(2018, 9, 29, 0, 0)]
    quarter3 = [datetime(2018, 9, 28, 0, 0),
                datetime(2018, 9, 27, 0, 0), datetime(2018, 9, 26, 0, 0), datetime(2018, 9, 25, 0, 0),
                datetime(2018, 9, 24, 0, 0), datetime(2018, 9, 23, 0, 0), datetime(2018, 9, 22, 0, 0),
                datetime(2018, 9, 21, 0, 0), datetime(2018, 9, 20, 0, 0), datetime(2018, 9, 19, 0, 0),
                datetime(2018, 9, 18, 0, 0), datetime(2018, 9, 17, 0, 0), datetime(2018, 9, 16, 0, 0),
                datetime(2018, 9, 15, 0, 0), datetime(2018, 9, 14, 0, 0), datetime(2018, 9, 13, 0, 0),
                datetime(2018, 9, 12, 0, 0), datetime(2018, 9, 11, 0, 0), datetime(2018, 9, 10, 0, 0),
                datetime(2018, 9, 9, 0, 0), datetime(2018, 9, 8, 0, 0), datetime(2018, 9, 7, 0, 0),
                datetime(2018, 9, 6, 0, 0), datetime(2018, 9, 5, 0, 0), datetime(2018, 9, 4, 0, 0),
                datetime(2018, 9, 3, 0, 0), datetime(2018, 9, 2, 0, 0), datetime(2018, 9, 1, 0, 0),
                datetime(2018, 8, 31, 0, 0), datetime(2018, 8, 30, 0, 0), datetime(2018, 8, 29, 0, 0),
                datetime(2018, 8, 28, 0, 0), datetime(2018, 8, 27, 0, 0), datetime(2018, 8, 26, 0, 0),
                datetime(2018, 8, 25, 0, 0), datetime(2018, 8, 24, 0, 0), datetime(2018, 8, 23, 0, 0),
                datetime(2018, 8, 22, 0, 0), datetime(2018, 8, 21, 0, 0), datetime(2018, 8, 20, 0, 0),
                datetime(2018, 8, 19, 0, 0), datetime(2018, 8, 18, 0, 0), datetime(2018, 8, 17, 0, 0),
                datetime(2018, 8, 16, 0, 0), datetime(2018, 8, 15, 0, 0), datetime(2018, 8, 14, 0, 0),
                datetime(2018, 8, 13, 0, 0), datetime(2018, 8, 12, 0, 0), datetime(2018, 8, 11, 0, 0),
                datetime(2018, 8, 10, 0, 0), datetime(2018, 8, 9, 0, 0), datetime(2018, 8, 8, 0, 0),
                datetime(2018, 8, 7, 0, 0), datetime(2018, 8, 6, 0, 0), datetime(2018, 8, 5, 0, 0),
                datetime(2018, 8, 4, 0, 0), datetime(2018, 8, 3, 0, 0), datetime(2018, 8, 2, 0, 0),
                datetime(2018, 8, 1, 0, 0), datetime(2018, 7, 31, 0, 0), datetime(2018, 7, 30, 0, 0),
                datetime(2018, 7, 29, 0, 0), datetime(2018, 7, 28, 0, 0), datetime(2018, 7, 27, 0, 0),
                datetime(2018, 7, 26, 0, 0), datetime(2018, 7, 25, 0, 0), datetime(2018, 7, 24, 0, 0),
                datetime(2018, 7, 23, 0, 0), datetime(2018, 7, 22, 0, 0), datetime(2018, 7, 21, 0, 0),
                datetime(2018, 7, 20, 0, 0), datetime(2018, 7, 19, 0, 0), datetime(2018, 7, 18, 0, 0),
                datetime(2018, 7, 17, 0, 0), datetime(2018, 7, 16, 0, 0), datetime(2018, 7, 15, 0, 0),
                datetime(2018, 7, 14, 0, 0), datetime(2018, 7, 13, 0, 0), datetime(2018, 7, 12, 0, 0),
                datetime(2018, 7, 11, 0, 0), datetime(2018, 7, 10, 0, 0), datetime(2018, 7, 9, 0, 0),
                datetime(2018, 7, 8, 0, 0), datetime(2018, 7, 7, 0, 0), datetime(2018, 7, 6, 0, 0),
                datetime(2018, 7, 5, 0, 0), datetime(2018, 7, 4, 0, 0), datetime(2018, 7, 3, 0, 0),
                datetime(2018, 7, 2, 0, 0), datetime(2018, 7, 1, 0, 0), datetime(2018, 6, 30, 0, 0)]
    quarter4 = [datetime(2018, 6, 29, 0, 0), datetime(2018, 6, 28, 0, 0), datetime(2018, 6, 27, 0, 0),
                datetime(2018, 6, 26, 0, 0), datetime(2018, 6, 25, 0, 0), datetime(2018, 6, 24, 0, 0),
                datetime(2018, 6, 23, 0, 0), datetime(2018, 6, 22, 0, 0), datetime(2018, 6, 21, 0, 0),
                datetime(2018, 6, 20, 0, 0), datetime(2018, 6, 19, 0, 0), datetime(2018, 6, 18, 0, 0),
                datetime(2018, 6, 17, 0, 0), datetime(2018, 6, 16, 0, 0), datetime(2018, 6, 15, 0, 0),
                datetime(2018, 6, 14, 0, 0), datetime(2018, 6, 13, 0, 0), datetime(2018, 6, 12, 0, 0),
                datetime(2018, 6, 11, 0, 0), datetime(2018, 6, 10, 0, 0), datetime(2018, 6, 9, 0, 0),
                datetime(2018, 6, 8, 0, 0), datetime(2018, 6, 7, 0, 0), datetime(2018, 6, 6, 0, 0),
                datetime(2018, 6, 5, 0, 0), datetime(2018, 6, 4, 0, 0), datetime(2018, 6, 3, 0, 0),
                datetime(2018, 6, 2, 0, 0), datetime(2018, 6, 1, 0, 0), datetime(2018, 5, 31, 0, 0),
                datetime(2018, 5, 30, 0, 0), datetime(2018, 5, 29, 0, 0), datetime(2018, 5, 28, 0, 0),
                datetime(2018, 5, 27, 0, 0), datetime(2018, 5, 26, 0, 0), datetime(2018, 5, 25, 0, 0),
                datetime(2018, 5, 24, 0, 0), datetime(2018, 5, 23, 0, 0), datetime(2018, 5, 22, 0, 0),
                datetime(2018, 5, 21, 0, 0), datetime(2018, 5, 20, 0, 0), datetime(2018, 5, 19, 0, 0),
                datetime(2018, 5, 18, 0, 0), datetime(2018, 5, 17, 0, 0), datetime(2018, 5, 16, 0, 0),
                datetime(2018, 5, 15, 0, 0), datetime(2018, 5, 14, 0, 0), datetime(2018, 5, 13, 0, 0),
                datetime(2018, 5, 12, 0, 0), datetime(2018, 5, 11, 0, 0), datetime(2018, 5, 10, 0, 0),
                datetime(2018, 5, 9, 0, 0), datetime(2018, 5, 8, 0, 0), datetime(2018, 5, 7, 0, 0),
                datetime(2018, 5, 6, 0, 0), datetime(2018, 5, 5, 0, 0), datetime(2018, 5, 4, 0, 0),
                datetime(2018, 5, 3, 0, 0), datetime(2018, 5, 2, 0, 0), datetime(2018, 5, 1, 0, 0),
                datetime(2018, 4, 30, 0, 0), datetime(2018, 4, 29, 0, 0), datetime(2018, 4, 28, 0, 0),
                datetime(2018, 4, 27, 0, 0), datetime(2018, 4, 26, 0, 0), datetime(2018, 4, 25, 0, 0),
                datetime(2018, 4, 24, 0, 0), datetime(2018, 4, 23, 0, 0), datetime(2018, 4, 22, 0, 0),
                datetime(2018, 4, 21, 0, 0), datetime(2018, 4, 20, 0, 0), datetime(2018, 4, 19, 0, 0),
                datetime(2018, 4, 18, 0, 0), datetime(2018, 4, 17, 0, 0), datetime(2018, 4, 16, 0, 0),
                datetime(2018, 4, 15, 0, 0), datetime(2018, 4, 14, 0, 0), datetime(2018, 4, 13, 0, 0),
                datetime(2018, 4, 12, 0, 0), datetime(2018, 4, 11, 0, 0), datetime(2018, 4, 10, 0, 0),
                datetime(2018, 4, 9, 0, 0), datetime(2018, 4, 8, 0, 0), datetime(2018, 4, 7, 0, 0),
                datetime(2018, 4, 6, 0, 0), datetime(2018, 4, 5, 0, 0), datetime(2018, 4, 4, 0, 0),
                datetime(2018, 4, 3, 0, 0), datetime(2018, 4, 2, 0, 0), datetime(2018, 4, 1, 0, 0),
                datetime(2018, 3, 31, 0, 0)]
    assert list_of_quarters == [quarter1, quarter2, quarter3, quarter4]
