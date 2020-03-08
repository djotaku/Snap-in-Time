"""Thin out the snapshots on disk."""


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
    pass
