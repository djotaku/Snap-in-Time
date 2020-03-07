"""Test remote backup functions."""

import subprocess
from unittest import mock

from snapintime import remote_backup


@mock.patch('snapintime.remote_backup.subprocess')
def test_get_remote_latest_subvol(subprocess_mock):
    subprocess_done = subprocess.CompletedProcess(args="args", returncode=0, stdout="2019-06-27\n2019-07-31\n2019-08-30\n2019-09-23\n2019-09-26\n2019-10-01\n2019-10-04\n2019-10-07\n2019-10-10\n2019-10-11\n2019-10-14\n2019-10-16\n2019-10-22\n2019-10-23\n2019-10-27\n2019-10-29\n2019-10-30\n2019-11-03\n2019-11-06\n2019-11-07\n2019-11-15\n2019-11-17\n2019-11-19\n2019-11-22\n2019-11-24\n2019-12-01\n2019-12-01p2\n2019-12-03\n2019-12-06\n2019-12-12\n2019-12-19\n2019-12-26\n2019-12-28\n2020-01-01\n2020-01-02\n2020-01-04\n2020-01-06\n2020-01-08\n2020-01-09\n2020-01-16\n2020-01-30\n2020-02-03\n2020-02-03p2\n2020-02-10\n2020-02-10p2\n2020-02-11\n2020-02-17\n2020-02-20\n2020-02-20p2\n2020-02-25\n2020-03-01\n2020-03-05-2022\n")
    subprocess_mock.run.return_value = subprocess_done
    result = remote_backup.get_remote_latest_subvol("user@remote", "/media/backup")
    assert result == "2020-03-05-2022"
