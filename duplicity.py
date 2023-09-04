import os
from subprocess import Popen, PIPE
from dotenv import load_dotenv

load_dotenv()


def dupe_backup(dir: str, url: str):
    if os.path.isdir(dir):
        p = Popen(["duplicity", "bu", dir, url], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print(p)
        # output = p.communicate(input=pf)[0].decode()
        # print("wioefjiowejfiowjef", output)
    else:
        print("Not a directory")


if __name__ == "__main__":
    url = os.getenv("DUPE_URL")
    dupe_backup("test_dir", url)
