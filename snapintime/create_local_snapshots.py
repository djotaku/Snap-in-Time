"""Read in configuration file and create local snapshots."""

import subprocess
from datetime import datetime

from snapintime.utils import config as config  # type: ignore


def get_date_time() -> str:
    """Return the current time, uses system time zone."""
    now: datetime = datetime.now()
    return now.strftime("%Y-%m-%d-%H%M")


def iterate_configs(date_time: str, config: dict) -> list:
    """Iterate over all the subvolumes in the config file, then call\
    create_snapshot.

    :param date_time: The date time that will end up as the btrfs snapshot name
    :param config: The config file, parsed by import_config.
    :returns: A list containing return values from create_snapshot
    """
    return [
        create_snapshot(
            date_time, subvol.get("subvol"), subvol.get("backuplocation")
        )
        for subvol in config.values()
    ]


def create_snapshot(date_suffix: str, subvol: str, backup_location: str):
    """Create a btrfs snapshot.

    :param date_suffix: a datetime object formatted to be the name of the snapshot
    :param subvol: The subvolume to be snapshotted
    :param backup_location: The folder in which to create the snapshot
    """
    command = f"/usr/sbin/btrfs sub snap -r {subvol} {backup_location}/{date_suffix}"
    try:
        raw_result = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
        return {
            "Command": raw_result.args,
            "Return Code": raw_result.returncode,
            "Output": raw_result.stdout,
        }

    except subprocess.CalledProcessError as e:
        return {
            "Command": e.args[1],
            "Return Code": {e.returncode},
            "Output": str(e.stderr),
        }


def main():  # pragma: no cover
    date_time_for_backup = get_date_time()
    our_config = config.import_config()
    results = iterate_configs(date_time_for_backup, our_config)
    for result in results:
        print(f"\nRan {result['Command']} with a return code of {result['Return Code']}")
        print(f"Result was: {str(result['Output'])}\n")


if __name__ == "__main__":  # pragma: no cover
    main()
