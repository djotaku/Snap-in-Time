"""Thin out the snapshots on disk."""

from datetime import datetime
import itertools
import os
import re
import subprocess

from snapintime.utils import config as config  # type: ignore
import snapintime.utils.date  # type: ignore


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


def get_subvols_by_date(directory: str, reg_ex) -> list:
    """Return a list based on matching regular expression.

    This is meant to produce the list that will be the input for one of the culling functions.

    :param directory: The directory we want to grab subvols from.
    :param reg_ex: A regular expression to apply to the directory contents.
    :returns: A list of subvolumes for culling.
    """
    subvols = os.listdir(path=directory)
    return_list = []
    for subvol in subvols:
        if reg_ex.search(subvol) is not None:
            return_list.append(subvol)
    return return_list


def btrfs_del(directory: str, subvols: list) -> list:
    """Delete subvolumes in a given directory.

    :param directory: The directory holding the subvolumes.
    :param subvols: A list of subvolumes to delete
    :returns: A list with the commands run and the results or, if there weren't any subvolumes\
    to delete, returns a message with that information.
    """
    return_list = []
    if len(subvols) > 0:
        for subvol in subvols:
            command = f"/usr/sbin/btrfs sub del {directory}/{subvol}"
            try:
                raw_result = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
                return_text = f"Ran {raw_result.args} with a return code of {raw_result.returncode}.\n"\
                    f"Result was {str(raw_result.stdout)}"
                return_list.append(return_text)
            except subprocess.SubprocessError as e:
                error_text = f"Ran {e.args} with a return code of {e.returncode}.\n Result was {str(e.stderr)}"  # type: ignore
                return_list.append(error_text)
    else:
        return_list = ["There was either only one or no subvolumes at that date"]
    return return_list


def cull_three_days_ago(config: dict) -> list:
    """Cull the btrfs snapshots from 3 days ago.

    :param config: The configuration file.
    :returns: A list containing the results of running the commands.
    """
    three_days_ago: str = snapintime.utils.date.prior_date(datetime.now(), 3).strftime("%Y-%m-%d")
    three_days_ago_reg_ex = re.compile(three_days_ago)
    return_list = []
    for subvol in config.values():
        subvols_three_days_ago = get_subvols_by_date(subvol.get("backuplocation"), three_days_ago_reg_ex)
        three_days_ago_culled = daily_cull(subvols_three_days_ago)
        return_list.append(btrfs_del(subvol.get("backuplocation"), three_days_ago_culled))
    return return_list


def main():  # pragma: no cover
    our_config = config.import_config()
    three_day_cull_result = cull_three_days_ago(our_config)
    print(three_day_cull_result)
    # grab dir <- universal
    # regex to date we want to cull <- universal
    # call daily_cull <- only for daily_cull
    # take those results and, if not emtpy list, btrfs del the list <- universal


if __name__ == "__main__":  # pragma: no cover
    main()
