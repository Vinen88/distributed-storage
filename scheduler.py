import schedule
from time import sleep


def do_backup(job: callable, minutes: str):
    # minutes should be in the form of "(:MM)"
    schedule.every().hour.at(minutes).do(job)
    while True:
        schedule.run_pending()
        sleep(1)
