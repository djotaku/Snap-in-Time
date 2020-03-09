"""Test ability to create local snapshots."""

from datetime import datetime
import subprocess
from unittest import mock

from snapintime import create_local_snapshots


@mock.patch('snapintime.create_local_snapshots.datetime')
def test_correct_date_time(datetime_mock):
    datetime_mock.now.return_value = datetime(2020, 1, 1, 12, 33)
    time_to_test = create_local_snapshots.get_date_time()
    assert time_to_test == "2020-01-01-1233"


def test_iterate_configs():
    pass


@mock.patch('snapintime.create_local_snapshots.subprocess')
def test_create_snapshot(subprocess_mock):
    subprocess_done = subprocess.CompletedProcess(args="args", returncode=0, stdout="stdout")
    subprocess_mock.run.return_value = subprocess_done
    result = create_local_snapshots.create_snapshot("2020-01-01-1233", "subvol", "backuplocation")
    assert result == {"Command": "args", "Return Code": 0, "Output": "stdout"}
