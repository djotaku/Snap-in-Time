"""Thin out the snapshots on disk."""

import itertools
import os
import re
import subprocess
from datetime import datetime
from typing import Pattern

import snapintime.utils.date  # type: ignore
from snapintime.utils import config as config  # type: ignore

from . import log


def split_dir_hours(subvols: list, reg_ex) -> list:
    """Return a list based on matching regular expression.

    :param subvols: A list of subvolumes.
    :param reg_ex: A re object defining the regular expression to evaluate against.
    :returns: A list that has only the items that passed the regular expression.
    """
    return [subvol for subvol in subvols if reg_ex.search(subvol) is not None]


def get_subvols_by_date(directory: str, reg_ex, remote: bool = False, remote_location: str = "") -> list:
    """Return a list based on matching regular expression.

    This is meant to produce the list that will be the input for one of the culling functions.

    :param remote_location: This should be a string like user@computer or user@IPaddress
    :param remote: True if this is taking place on the remote system
    :param directory: The directory we want to grab subvols from.
    :param reg_ex: A regular expression to apply to the directory contents.
    :returns: A list of subvolumes for culling.
    """
    if remote and remote_location:
        command = f"ssh {remote_location} ls {directory}"
        results = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
        subvols = results.stdout.split('\n')
    else:
        subvols = os.listdir(path=directory)
    return [subvol for subvol in subvols if reg_ex.search(subvol) is not None]


def btrfs_del(directory: str, subvols: list, remote: bool = False, remote_location: str = "") -> list:
    """Delete subvolumes in a given directory.

    :param remote_location: This should be a string like user@computer or user@IPaddress
    :param remote: If True, working on remote system
    :param directory: The directory holding the subvolumes.
    :param subvols: A list of subvolumes to delete
    :returns: A list with the commands run and the results or, if there weren't any subvolumes\
    to delete, returns a message with that information.
    """
    return_list = []
    if subvols:
        for subvol in subvols:
            if remote and remote_location:
                command = f"ssh {remote_location} /usr/sbin/btrfs sub del {directory}/{subvol}"
            else:
                command = f"/usr/sbin/btrfs sub del {directory}/{subvol}"
            try:
                log.debug(f'{remote=}')
                log.debug(f'{remote_location=}')
                log.debug(f'{command=}')
                raw_result = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
                return_text = f"Ran {raw_result.args} with a return code of {raw_result.returncode}.\n" \
                              f"Result was {str(raw_result.stdout)}"
                return_list.append(return_text)
            except subprocess.SubprocessError as e:
                error_text = f"Ran {e.args[1]} with a return code of {e.returncode}.\nResult was {str(e.stderr)}"  # type: ignore
                return_list.append(error_text)
    else:
        return_list = ["There was either only one or no subvolumes at that date"]
    return return_list


def generate_daily_cull_list(dir_to_cull: list) -> list:
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
    fourths: list[Pattern[str]] = [re.compile(r'0[0-5]\d\d$'),
                                   re.compile(r'0[6-9]\d\d$|1[0-1]\d\d$'),
                                   re.compile(r'1[2-7]\d\d$'),
                                   re.compile(r'1[8-9]\d\d$|2[0-3]\d\d$')]
    fourths_list = [split_dir_hours(dir_to_cull, fourth)[1:] for fourth in fourths]
    return list(itertools.chain.from_iterable(fourths_list))


def cull_three_days_ago(config: dict) -> list:
    """Cull the btrfs snapshots from 3 days ago.

    Take snapshots that were taken on the third day in the past and cull to 4 (max) snapshots.

    :param config: The configuration file.
    :returns: A list containing the results of running the commands.
    """
    location: str = "backuplocation"
    three_days_ago: str = snapintime.utils.date.prior_date(datetime.now(), 3).strftime("%Y-%m-%d")
    three_days_ago_reg_ex = re.compile(three_days_ago)
    return_list = []
    for subvol in config.values():
        subvols_three_days_ago = get_subvols_by_date(subvol.get(location), three_days_ago_reg_ex)
        three_days_ago_culled = generate_daily_cull_list(subvols_three_days_ago)
        return_list.append(btrfs_del(subvol.get(location), three_days_ago_culled))
    return return_list


def generate_weekly_cull_list(dir_to_cull: list) -> list:
    """Take a list of snapshots from a directory (already reduced to one day) and cull.

        This culling will return a list with the snapshots to remove for the given day.

        For a perfect set of snapshots, (where the user has been doing one snapshot per hour and \
        doing the daily culling) it should leave behind (remove from list):

        - day1-1800

        :param dir_to_cull: A list containing snapshots. Assumes another function\
        has already reduced this list to a list containing only one week's worth of\
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
        seven_days_ago_culled = generate_weekly_cull_list(subvols_seven_days_ago)
        return_list.append(btrfs_del(subvol.get("backuplocation"), seven_days_ago_culled))
    return return_list


def generate_quarterly_yearly_cull_list(dir_to_cull: list) -> list:
    """Take a list of snapshots from a directory (already reduced to one week or quarter) and cull.

            This culling will return a list with the snapshots to remove for the week or quarter.

            For a perfect set of snapshots, (where the user has been doing one snapshot per hour and \
            doing the daily culling) it should leave behind (remove from list):

            - day7-1800

            .. note:: May end up combining with weekly cull as they essentially do the same thing.

            :param dir_to_cull: A list containing snapshots. Assumes another function\
            has already reduced this list to a list containing only one week or quarter's worth of\
            snapshots.
            :returns: A list containing all the subvolumes to cull.
            """
    sorted_dir_to_cull = sorted(dir_to_cull)
    if len(sorted_dir_to_cull) != 0:
        sorted_dir_to_cull.pop()
    return sorted_dir_to_cull


def remove_protected(subvol: dict, subvol_list_to_pare: list):
    protected_snapshots = subvol.get("remote_protected")
    if protected_snapshots is None:
        protected_snapshots = []
    return [subvol for subvol in subvol_list_to_pare if subvol not in protected_snapshots]


def cull_last_quarter(config: dict, remote: bool = False) -> list:
    """Cull the btrfs snapshots from quarter.

    Should leave 1 snapshot per week for 13 weeks.

    :param remote: Are we doing this on the remote system?
    :param config: The configuration file.
    :returns: A list containing the results of running the commands.
    """
    last_quarter: list = snapintime.utils.date.quarterly_weeks(datetime.now())
    location: str = "remote_subvol_dir" if remote else "backuplocation"
    return_list = []
    for subvol in config.values():
        for week in last_quarter:
            reg_ex_string = ""
            for day in week:
                reg_ex_string = f"{reg_ex_string}({day.strftime('%Y-%m-%d')})|"
            reg_ex_string_minus_final_or = reg_ex_string[:-1]
            weekly_reg_ex = re.compile(reg_ex_string_minus_final_or)
            subvols_this_week = get_subvols_by_date(subvol.get(location), weekly_reg_ex,
                                                    remote, subvol.get("remote_location"))
            if remote:
                subvols_this_week = remove_protected(subvol, subvols_this_week)
            if len(subvols_this_week) != 0:
                this_week_culled = generate_quarterly_yearly_cull_list(subvols_this_week)
                return_list.append(btrfs_del(subvol.get(location), this_week_culled, remote,
                                             remote_location=subvol.get('remote_location')))
    return return_list


def cull_last_year(config: dict, remote: bool = False) -> list:
    """Cull the btrfs snapshots from quarter.

    Should leave 1 snapshot per quarter for 4 quarters.

    :param remote: If true, we're doing this on the remote system.
    :param config: The configuration file.
    :returns: A list containing the results of running the commands.
    """
    last_year: list = snapintime.utils.date.yearly_quarters(datetime.now())
    return_list = []
    for subvol in config.values():
        for quarter in last_year:
            reg_ex_string = ""
            for day in quarter:
                reg_ex_string = f"{reg_ex_string}({day.strftime('%Y-%m-%d')})|"
            reg_ex_string_minus_final_or = reg_ex_string[:-1]
            quarterly_reg_ex = re.compile(reg_ex_string_minus_final_or)
            subvols_this_quarter = get_subvols_by_date(subvol.get("backuplocation"), quarterly_reg_ex)
            if remote:
                subvols_this_quarter = remove_protected(subvol, subvols_this_quarter)
            if len(subvols_this_quarter) != 0:
                this_quarter_culled = generate_quarterly_yearly_cull_list(subvols_this_quarter)
                return_list.append(btrfs_del(subvol.get("backuplocation"), this_quarter_culled, remote,
                                             remote_location=subvol.get('remote_location')))
    return return_list


def print_output(list_of_lists: list):  # pragma: no cover
    for directory in list_of_lists:
        for result in directory:
            log.info(result)


def main():  # pragma: no cover
    our_config = config.import_config()
    three_day_cull_result = cull_three_days_ago(our_config)
    print_output(three_day_cull_result)
    seven_day_cull_result = cull_seven_days_ago(our_config)
    print_output(seven_day_cull_result)
    quarter_cull_result = cull_last_quarter(our_config)
    print_output(quarter_cull_result)
    year_cull_result = cull_last_year(our_config)
    print_output(year_cull_result)


if __name__ == "__main__":  # pragma: no cover
    main()
