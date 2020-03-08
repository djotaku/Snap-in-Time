"""Thin out the snapshots on disk."""

import itertools
import re


def split_dir_hours(subvols: list, reg_ex) -> list:
    """Return a list based on matching regular expression.

    :param subvols: A list of subvolumes.
    :param reg_ex: A re object defining the regular expression to evaluate against.
    :returns: A list that has only the items that passed the regular expression.
    """
    return_list = []
    for subvol in subvols:
        if reg_ex.search(subvol) is not None:
            return_list.append(subvol)
    return return_list


def daily_cull(dir_to_cull: list) -> list:
    """Take a list of snapshots from a directory (already reduced to one day) and cull.

    This culling will produce the closest it can to 4 snapshots\
    for that day.

    For a perfect set of 24 snapshots, it should leave behind (remove from list):

    - day1-0000
    - day1-0600
    - day1-1200
    - day1-1800

    :param dir_to_cull: A list containing snapshots. Assumes another function\
    has already reduced this list to a list containing only one day's worth of\
    snapshots.
    :returns: A list containing all the subvolumes to cull.
    """
    fourths = [re.compile('[0][0-5][0-9][0-9]$'), re.compile('[0][6-9][0-9][0-9]$|[1][0-1][0-9][0-9]$'), re.compile('[1][2-7][0-9][0-9]$'), re.compile('[1][8-9][0-9][0-9]$|[2][0-3][0-9][0-9]$')]
    fourths_list = []
    for fourth in fourths:
        fourths_list.append(split_dir_hours(dir_to_cull, fourth)[1:])
    return list(itertools.chain.from_iterable(fourths_list))


def main():  # pragma: no cover
    hourly_dir_to_cull = ["2020-03-01-0000", "2020-03-01-0100", "2020-03-01-0200", "2020-03-01-0300", "2020-03-01-0400", "2020-03-01-0500", "2020-03-01-0600", "2020-03-01-0700", "2020-03-01-0800", "2020-03-01-0900", "2020-03-01-1000", "2020-03-01-1100", "2020-03-01-1200", "2020-03-01-1300", "2020-03-01-1400", "2020-03-01-1500", "2020-03-01-1600", "2020-03-01-1700", "2020-03-01-1800", "2020-03-01-1900", "2020-03-01-2000", "2020-03-01-2100", "2020-03-01-2200", "2020-03-01-2300"]
    print(daily_cull(hourly_dir_to_cull))


if __name__ == "__main__":  # pragma: no cover
    main()
