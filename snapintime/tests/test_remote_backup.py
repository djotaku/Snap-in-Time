"""Test remote backup functions."""

import subprocess
from unittest import mock

from snapintime import remote_backup


@mock.patch('snapintime.remote_backup.subprocess')
def test_get_remote_latest_subvol(subprocess_mock):
    subprocess_done = subprocess.CompletedProcess(args="args", returncode=0, stdout="2020-02-11\n2020-02-17\n2020-02-20\n2020-02-20p2\n2020-02-25\n2020-03-01\n2020-03-05-2022\n")
    subprocess_mock.run.return_value = subprocess_done
    result = remote_backup.get_remote_subvols("user@remote", "/media/backup")
    assert result == ["2020-02-11", "2020-02-17", "2020-02-20", "2020-02-20p2", "2020-02-25", "2020-03-01", "2020-03-05-2022", '']


@mock.patch('snapintime.remote_backup.os')
def test_get_local_subvols(os_mock):
    mock_return = ["2020-02-11", "2020-02-17", "2020-02-20", "2020-02-20p2", "2020-02-25", "2020-03-01", "2020-03-05-2022"]
    os_mock.listdir.return_value = mock_return
    result = remote_backup.get_local_subvols('/dir')
    assert result == ["2020-02-11", "2020-02-17", "2020-02-20", "2020-02-20p2", "2020-02-25", "2020-03-01", "2020-03-05-2022"]


def test_match_subvols_oldest_remote_is_there():
    """This should not trigger the recursion.

    The final value in the sorted remote list is in the local list.
    """
    local_list = ["A", "B", "C", "D"]
    remote_list = ["A", "B", "C"]
    result = remote_backup.match_subvols(local_list, remote_list)
    assert result == "C"


def test_match_subvols_oldest_remote_not_there():
    """This should trigger the recursion.

    The final value in the sorted remote list is not in the local list.
    """
    local_list = ["A", "B", "D"]
    remote_list = ["A", "B", "C"]
    result = remote_backup.match_subvols(local_list, remote_list)
    assert result == "B"


def test_btrfs_send_receive():
    pass


def test_iterate_configs():
    pass
