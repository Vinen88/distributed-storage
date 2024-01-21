#!/usr/bin/env python3

import schedule
from time import sleep
from typing import Callable
import sys
import duplicity
from install import create_service


def main():
    print("Service is now running! Woohoo :)", file=sys.stderr)
    do_backup(duplicity.Duplicity("config.toml").dupe_backup, ":00")


def do_backup(job: Callable, minutes: str):
    # minutes should be in the form of "(:MM)"
    schedule.every().hour.at(minutes).do(job)
    while True:
        schedule.run_pending()
        sleep(600)


if __name__ == "__main__" and not sys.flags.interactive:
    if len(sys.argv) > 1 and sys.argv[1] == "install-client":
        create_service()
    else:
        main()
