"""Read in configuration file and create local snapshots."""

from datetime import datetime
import subprocess

from snapintime.utils import config as config  # type: ignore


def get_date_time() -> str:
    """Return the current time, uses system time zone."""
    now: datetime = datetime.now()
    date_suffix: str = now.strftime("%Y-%m-%d-%H%M")
    return date_suffix


def iterate_configs(date_time: str, config: dict) -> list:
    """Iterate over all the subvolumes in the config file, then call\
    create_snapshot.

    :param date_time: The date time that will end up as the btrfs snapshot name
    :param config: The config file, parsed by import_config.
    :returns: A list containing return values from create_snapshot
    """
    return_list = []
    for subvol in config.values():
        return_list.append(create_snapshot(date_time, subvol.get("subvol"),
                                           subvol.get("backuplocation")))
    return return_list


def create_snapshot(date_suffix: str, subvol: str, backup_location: str):
    """Create a btrfs snapshot.

    :param date_suffix: a datetime object formatted to be the name of the snapshot
    :param subvol: The subvolume to be snapshotted
    :param backup_location: The folder in which to create the snapshot
    """
    command = f"/usr/sbin/btrfs sub snap -r {subvol} {backup_location}/{date_suffix}"
    raw_result = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
    #  because check=True, need to do in a try, except and do something with the error
    result = {"Command": raw_result.args, "Return Code": raw_result.returncode, "Output": raw_result.stdout}
    return result


def main():  # pragma: no cover
    date_time_for_backup = get_date_time()
    our_config = config.import_config()
    results = iterate_configs(date_time_for_backup, our_config)
    for result in results:
        print(f"\nRan {result['Command']} with a return code of {result['Return Code']}")
        print(f"Result was: {str(result['Output'])}\n")


if __name__ == "__main__":  # pragma: no cover
    main()
