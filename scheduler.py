import schedule
from time import sleep
from typing import Callable


def do_backup(job: Callable, minutes: str):
    # minutes should be in the form of "(:MM)"
    schedule.every().hour.at(minutes).do(job)
    while True:
        schedule.run_pending()
        sleep(1)
