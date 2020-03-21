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
                error_text = f"Ran {e.args[1]} with a return code of {e.returncode}.\nResult was {str(e.stderr)}"  # type: ignore
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


def weekly_cull(dir_to_cull: list) -> list:
    """Take a list of snapshots from a directory (already reduced to one day) and cull.

        This culling will return a list with the snapshots to remove for the given day.

        For a perfect set of snapshots, (where the user has been doing one snapshot per hour and \
        doing the daily culling) it should leave behind (remove from list):

        - day1-1800

        :param dir_to_cull: A list containing snapshots. Assumes another function\
        has already reduced this list to a list containing only one day's worth of\
        snapshots.
        :returns: A list containing all the subvolumes to cull.
        """
    sorted_dir_to_cull = sorted(dir_to_cull)
    if len(sorted_dir_to_cull) != 0:
        sorted_dir_to_cull.pop()
    return sorted_dir_to_cull


def cull_seven_days_ago(config: dict) -> list:
    """Cull the btrfs snapshots from 7 days ago.

    :param config: The configuration file.
    :returns: A list containing the results of running the commands.
    """
    seven_days_ago: str = snapintime.utils.date.prior_date(datetime.now(), 7).strftime("%Y-%m-%d")
    seven_days_ago_reg_ex = re.compile(seven_days_ago)
    return_list = []
    for subvol in config.values():
        subvols_seven_days_ago = get_subvols_by_date(subvol.get("backuplocation"), seven_days_ago_reg_ex)
        seven_days_ago_culled = weekly_cull(subvols_seven_days_ago)
        return_list.append(btrfs_del(subvol.get("backuplocation"), seven_days_ago_culled))
    return return_list


def quarterly_cull(dir_to_cull: list) -> list:
    """Take a list of snapshots from a directory (already reduced to one week) and cull.

            This culling will return a list with the snapshots to remove for the week.

            For a perfect set of snapshots, (where the user has been doing one snapshot per hour and \
            doing the daily culling) it should leave behind (remove from list):

            - day7-1800

            .. note:: May end up combining with weekly cull as they essentially do the same thing.

            :param dir_to_cull: A list containing snapshots. Assumes another function\
            has already reduced this list to a list containing only one day's worth of\
            snapshots.
            :returns: A list containing all the subvolumes to cull.
            """
    sorted_dir_to_cull = sorted(dir_to_cull)
    if len(sorted_dir_to_cull) != 0:
        sorted_dir_to_cull.pop()
    return sorted_dir_to_cull


def cull_last_quarter(config: dict) -> list:
    """Cull the btrfs snapshots from quarter.

    Should leave 1 snapshot per week for 13 weeks.

    :param config: The configuration file.
    :returns: A list containing the results of running the commands.
    """
    last_quarter: list = snapintime.utils.date.quarterly_weeks(datetime.now())
    #last_quarter_reg_ex = re.compile(last_quarter)
    return_list = []
    for subvol in config.values():
        for week in last_quarter:
            reg_ex_string = ""
            for day in week:
                reg_ex_string = reg_ex_string + f'({day.strftime("%Y-%m-%d")})|'
            reg_ex_string_minus_final_or = reg_ex_string[:-1]
            weekly_reg_ex = re.compile(reg_ex_string_minus_final_or)
            subvols_this_week = get_subvols_by_date(subvol.get("backuplocation"), weekly_reg_ex)
            if len(subvols_this_week) != 0:
                this_week_culled = quarterly_cull(subvols_this_week)
                return_list.append(btrfs_del(subvol.get("backuplocation"), this_week_culled))
    return return_list


def print_output(list_of_lists: list):  # pragma: no cover
    for directory in list_of_lists:
        for result in directory:
            print(result)


def main():  # pragma: no cover
    our_config = config.import_config()
    three_day_cull_result = cull_three_days_ago(our_config)
    print_output(three_day_cull_result)
    seven_day_cull_result = cull_seven_days_ago(our_config)
    print_output(seven_day_cull_result)
    quarter_cull_result = cull_last_quarter(our_config)
    print_output(quarter_cull_result)
    # grab dir <- universal
    # regex to date we want to cull <- universal
    # call daily_cull <- only for daily_cull
    # take those results and, if not emtpy list, btrfs del the list <- universal


if __name__ == "__main__":  # pragma: no cover
    main()