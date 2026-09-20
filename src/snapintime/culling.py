"""Thin out the snapshots on disk."""

import os
import re
import subprocess
from datetime import datetime, timedelta
from typing import Optional

import snapintime.utils.date  # type: ignore
from snapintime.utils import config as config  # type: ignore

from . import log


SNAPSHOT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}$")
SNAPSHOT_FORMAT = "%Y-%m-%d-%H%M"


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


def btrfs_del(directory: str, subvols: list, remote: bool = False, remote_location: str = "") -> list[str]:
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
                              f"Result was {raw_result.stdout!s}"
                return_list.append(return_text)
            except subprocess.SubprocessError as e:
                error_text = f"Ran {e.args[1]} with a return code of {e.returncode}.\nResult was {e.stderr!s}"  # type: ignore
                return_list.append(error_text)
    else:
        return_list = [f"There was either only one or no subvolumes in {directory} at that date"]
    return return_list


def _parse_snapshots(snapshot_names: list) -> list[tuple[datetime, str]]:
    """Return valid snapshot names paired with their timestamps."""
    parsed_snapshots = []
    for snapshot_name in snapshot_names:
        if SNAPSHOT_RE.fullmatch(snapshot_name) is None:
            continue
        try:
            parsed_snapshots.append((datetime.strptime(snapshot_name, SNAPSHOT_FORMAT), snapshot_name))
        except ValueError:
            continue
    return sorted(parsed_snapshots)


def _closest_snapshot(snapshots: list[tuple[datetime, str]], target: datetime) -> str:
    """Return the snapshot closest to a representative time."""
    return min(snapshots, key=lambda snapshot: (abs(snapshot[0] - target), -snapshot[0].timestamp()))[1]


def generate_retention_cull_list(snapshot_names: list, now: datetime | None = None) -> list:
    """Return snapshots that fall outside the progressive retention policy.

    The policy retains all snapshots for two days, four representative snapshots
    per calendar day through seven days, one per calendar day through thirteen
    weeks, one per ISO week through one year, and one per calendar quarter after
    that. Invalid or non-snapshot directory entries are left untouched.
    """
    reference_time = now or datetime.now()
    parsed_snapshots = _parse_snapshots(snapshot_names)
    hourly_cutoff = timedelta(days=2)
    six_hour_cutoff = timedelta(days=7)
    daily_cutoff = timedelta(weeks=13)
    weekly_cutoff = timedelta(days=365)
    snapshots_by_group: dict[tuple, list[tuple[datetime, str]]] = {}
    retained = set()

    for snapshot_time, snapshot_name in parsed_snapshots:
        age = reference_time - snapshot_time
        if age < timedelta(0) or age < hourly_cutoff:
            retained.add(snapshot_name)
            continue

        if age < six_hour_cutoff:
            group = ("six-hour", snapshot_time.date())
        elif age < daily_cutoff:
            group = ("daily", snapshot_time.date())
        elif age < weekly_cutoff:
            group = ("weekly", snapintime.utils.date.iso_week(snapshot_time))
        else:
            group = ("quarterly", snapintime.utils.date.calendar_quarter(snapshot_time))
        snapshots_by_group.setdefault(group, []).append((snapshot_time, snapshot_name))

    for (frequency, period), snapshots in snapshots_by_group.items():
        if frequency == "six-hour":
            targets = [datetime.combine(period, datetime.min.time()).replace(hour=hour) for hour in (0, 6, 12, 18)]
        elif frequency == "daily":
            targets = [datetime.combine(period, datetime.min.time()).replace(hour=18)]
        elif frequency == "weekly":
            week_start = datetime.fromisocalendar(period[0], period[1], 1)
            targets = [week_start.replace(hour=18) + timedelta(days=6)]
        else:
            quarter_end = snapintime.utils.date.quarter_end(datetime(period[0], (period[1] - 1) * 3 + 1, 1))
            targets = [quarter_end.replace(hour=18)]

        for target in targets:
            if snapshots:
                retained.add(_closest_snapshot(snapshots, target))

    parsed_names = {snapshot_name for _, snapshot_name in parsed_snapshots}
    return [snapshot_name for snapshot_name in snapshot_names
            if snapshot_name in parsed_names and snapshot_name not in retained]


def cull_snapshots(configuration: dict, remote: bool = False, now: datetime | None = None) -> list:
    """Cull all configured snapshot directories using the retention policy."""
    location = "remote_subvol_dir" if remote else "backuplocation"
    return_list = []
    for subvol in configuration.values():
        directory = subvol.get(location)
        snapshots = get_subvols_by_date(directory, SNAPSHOT_RE, remote, subvol.get("remote_location"))
        snapshots_to_delete = generate_retention_cull_list(snapshots, now)
        if remote:
            snapshots_to_delete = remove_protected(subvol, snapshots_to_delete)
        if snapshots_to_delete:
            return_list.append(btrfs_del(directory, snapshots_to_delete, remote,
                                         remote_location=subvol.get("remote_location")))
    return return_list


def remove_protected(subvol: dict, subvol_list_to_pare: list):
    protected_snapshots = subvol.get("remote_protected")
    if protected_snapshots is None:
        protected_snapshots = []
    return [subvol for subvol in subvol_list_to_pare if subvol not in protected_snapshots]


def print_output(list_of_lists: list):  # pragma: no cover
    for directory in list_of_lists:
        for result in directory:
            log.info(result)


def main():  # pragma: no cover
    our_config = config.import_config()
    print_output(cull_snapshots(our_config))


if __name__ == "__main__":  # pragma: no cover
    main()
