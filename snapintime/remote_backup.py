"""Use btrfs send/receive to send snapshot to a remote computer."""

import subprocess


def get_remote_latest_subvol(remote_location: str, remote_subvol_dir: str) -> str:
    """This function assumes user has set up ssh keys for paswordless login.

    :param remote_location: This should be a string like user@computer or\
    user@IPaddress
    :param remote_subvol_dir: This is the directory we will search to get\
    the latest subvolume.
    """
    command = f"ssh {remote_location} ls {remote_subvol_dir}"
    results = subprocess.run(command, capture_output=True, shell=True, check=True, text=True)
    subvols = results.stdout.split('\n')
    sorted_subvols = sorted(subvols)
    return sorted_subvols[-1]


def main():  # pragma: no
    results = get_remote_latest_subvol("", "")
    print(results)


if __name__ == "__main__":  # pragma: no
    main()
