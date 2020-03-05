"""Read in configuration file and create local snapshots."""

from datetime import datetime
import json
import subprocess


def get_date_time() -> datetime:
    """Return the current time, uses system time zone."""
    return datetime.now()


def import_config() -> dict:
    """Import config file.

    :returns: A dictionary containing configs
    :raises: FileNotFoundError
    """
    try:
        with open("config.json") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Could not find config file.")


def iterate_configs(date_time: datetime, config: dict) -> list:
    """Iterate over all the subvolumes in the config file, then call\
    create_snapshot.

    :param date_time: The date time that will end up as the btrfs snapshot name
    :param config: The config file, parsed by import_config.
    :returns: A list containing return values from create_snapshot"""
    return_list = []
    for subvol in config.values():
        return_list.append(create_snapshot(date_time, subvol.get("subvol"),
                                           subvol.get("backuplocation")))
    return return_list


def create_snapshot(date_time: datetime, subvol: str, backup_location: str):
    date_suffix = date_time.strftime("%Y-%m-%d-%H%M") # maybe just have get_date_time return this?
    print(date_suffix)
    #  remember to use mroe advanced features of subprocess to know if command failed and to print what it's doing w/o needing to use all those print statements like you did last time.
    return date_suffix


def main():
    date_time_for_backup = get_date_time()
    config = import_config()
    results = iterate_configs(date_time_for_backup, config)
    print(results)


if __name__ == "__main__":
    main()
