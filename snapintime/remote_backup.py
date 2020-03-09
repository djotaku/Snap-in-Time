"""Use btrfs send/receive to send snapshot to a remote computer."""

import os
import subprocess

from snapintime.utils import config as config  # type: ignore


def get_remote_subvols(remote_location: str, remote_subvol_dir: str) -> list:
    """Retrieve the remote subvolumes.

    This function assumes user has set up ssh keys for paswordless login.

    :param remote_location: This should be a string like user@computer or\
    user@IPaddress
    :param remote_subvol_dir: This is the directory we will search to get\
    the latest subvolume.
    :returns: A list of the remove subvolumes.
    """
    command = f"ssh {remote_location} ls {remote_subvol_dir}"
    results = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
    subvols = results.stdout.split('\n')
    return subvols


def get_local_subvols(local_subvol_dir: str) -> list:
    """Grab the subvolumes from the local directory.

    :param local_subvol_dir: The directory containing the local subvolumes.
    :returns: A list of all the local subvolumes
    """
    subvols = os.listdir(path=local_subvol_dir)
    return subvols


def match_subvols(local_subvols: list, remote_subvols: list) -> str:
    """Return the latest remote subvol that also exists on the local system.

    :param local_subvols: A list of the local subvolumes.
    :param remote_subvols: A list of the remote subvolumes.
    :returns: The subvolume.
    """
    sorted_remote = sorted(remote_subvols)
    candidate = sorted_remote[-1]
    if candidate in local_subvols:
        return candidate
    else:
        sorted_remote.pop()
        return match_subvols(local_subvols, sorted_remote)


def btrfs_send_receive(local_subvols: list, remote_subvol: str, backup_location: str,
                       remote_location: str, remote_subvol_dir: str):
    """Run command to send/receive btrfs snapshot.

    :param local_subvols: A list of the local subvolumes to choose from.
    :param remote_subvol: The latest subvolume that is present on both the remote\
    and local systems.
    :param backup_location: The folder prefix for teh local_subvol
    :param remote_location: This should be a string like user@computer or\
    user@IPaddress
    :param remote_subvol_dir: This is the directory we will put the backup into on\
    the remote system.
    :returns: A dictionary with the result of the command.
    """
    sorted_local = sorted(local_subvols)
    command = f"/usr/sbin/btrfs send -p {backup_location}/{remote_subvol} {backup_location}/{sorted_local[-1]} | ssh {remote_location} btrfs receive {remote_subvol_dir}"
    try:
        raw_result = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
        result = {"Command": raw_result.args, "Return Code": raw_result.returncode, "Output": raw_result.stdout}
        return result
    except subprocess.SubprocessError as e:
        error_result = {"Command": e.args, "Return Code": e.returncode, "Output": e.stderr}  # type: ignore
        return error_result


def iterate_configs(config: dict) -> list:
    """Iterate over all the subvolumes in the config file, then call\
    btrfs_send_receive if the value of remote is "True".

    :param config: The config file, parsed by import_config.
    :returns: A list containing return values from btrfs_send_receive
    """
    return_list = []
    for subvol in config.values():
        if subvol.get("remote") == "True":
            remote_subvols = get_remote_subvols(subvol.get('remote_location'), subvol.get('remote_subvol_dir'))
            local_subvols = get_local_subvols(subvol.get("backuplocation"))
            match = match_subvols(local_subvols, remote_subvols)
            return_list.append(btrfs_send_receive(local_subvols, match, subvol.get('backuplocation'),
                                                  subvol.get('remote_location'), subvol.get('remote_subvol_dir')))
        else:
            pass
    return return_list


def main():  # pragma: no cover
    our_config = config.import_config()
    results = iterate_configs(our_config)
    for result in results:
        print(f"\nRan {result['Command']} with a return code of {result['Return Code']}")
        print(f"Result was: {str(result['Output'])}\n")


if __name__ == "__main__":  # pragma: no cover
    main()
