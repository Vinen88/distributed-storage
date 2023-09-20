#!/usr/bin/env python3

import schedule
from time import sleep
from typing import Callable
import os
import toml
from pathlib import Path
import sys
import duplicity

SERVICE_NAME = "distributed-storage.service"
SERVICE_PATH = str((Path("/etc/systemd/system/") / SERVICE_NAME).resolve())
THIS_DIR = (Path(__file__) / "..").resolve()


def main():
    # create_service()
    do_backup(duplicity.Duplicity("config.toml").dupe_backup, ":00")


def do_backup(job: Callable, minutes: str):
    # minutes should be in the form of "(:MM)"
    schedule.every().hour.at(minutes).do(job)
    while True:
        schedule.run_pending()
        sleep(1)


def create_service(venvdir: str):
    "creates a service"
    with open(SERVICE_PATH, "wt") as fo:
        toml.dump(
            {
                "Unit": {
                    "Description": "Duplicity backup service",
                },
                "Service": {
                    "User": os.getenv("USER"),
                    "WorkingDirectory": str(THIS_DIR),
                    "ExecStart": f"{venvdir}/bin/python -m {__file__}",
                },
                "Install": {
                    "WantedBy": "multi-user.target",
                },
            },
            fo,
        )
        os.system(f'systemctl enable "{SERVICE_NAME}"')
        os.system(f'systemctl start "{SERVICE_NAME}"')


if __name__ == "__main__" and not sys.flags.interactive:
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        create_service(sys.argv[2])
    else:
        main()
