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
