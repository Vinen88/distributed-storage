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
    print("Service is now running! Woohoo :)", file=sys.stderr)
    do_backup(duplicity.Duplicity("config.toml").dupe_backup, ":00")


def do_backup(job: Callable, minutes: str):
    # minutes should be in the form of "(:MM)"
    schedule.every().hour.at(minutes).do(job)
    while True:
        schedule.run_pending()
        sleep(600)


def create_service():
    "creates a service"
    text = (
        toml.dumps(
            {
                "Unit": {
                    "Description": "Duplicity backup service",
                },
                "Service": {
                    "User": os.getenv("USER"),
                    "WorkingDirectory": str(THIS_DIR),
                    "ExecStart": f"{str(THIS_DIR/'run_in_venv.bash')}",
                },
                "Install": {
                    "WantedBy": "multi-user.target",
                },
            },
        )
        .replace('"', "")
        .replace(" = ", "=")
    )
    with open(SERVICE_PATH, "wt", encoding="utf-8") as fo:
        fo.write(text)
    os.system(f'systemctl enable "{SERVICE_NAME}"')
    os.system(f'systemctl start "{SERVICE_NAME}"')


if __name__ == "__main__" and not sys.flags.interactive:
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        create_service()
    else:
        main()


