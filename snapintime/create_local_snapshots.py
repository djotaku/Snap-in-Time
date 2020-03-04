"""Read in configuration file and create local snapshots."""

import datetime
import json
import subprocess


def get_date_time():
    #  remember to use tzdata
    #  remember to just pass a datetime object because then you can just access like date.year
    #  rather than what you did last time. HOWEVER, need to make sure hour is formatted 24H time
    pass


def import_config():
    pass


def create_snapshot():
    #  remember to use mroe advanced features of subprocess to know if command failed and to print what it's doing w/o needing to use all those print statements like you did last time.
    pass


def main():
    import_config()
    create_snapshot()


if __name__ == "__main__":
    main()
