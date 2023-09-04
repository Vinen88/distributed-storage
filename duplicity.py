import os
import sys
from operator import itemgetter
from subprocess import Popen, PIPE
from dotenv import load_dotenv
import tomllib
from typing import Union, Literal
from functools import partial

load_dotenv()

Config = dict[Union[Literal["peers"], Literal["backup"]]]
eprint = partial(print, file=sys.stderr)


class Duplicity:
    def __init__(self, filepath) -> None:
        config = Duplicity.load_config(filepath)
        self.peers = Duplicity.get_some(config["peers"], "url")
        self.dirs = Duplicity.get_some(config["backups"], "dir")

    @staticmethod
    def load_config(filepath: str) -> Config:
        with open(filepath, "rb") as f:
            return tomllib.load(f)

    @staticmethod
    def get_some(config: dict, key: str) -> list:
        return tuple(map(itemgetter(key), config))

    def dupe_backup(self) -> None:
        for peer in self.peers:
            # ping peer
            for directory in self.dirs:
                if os.path.isdir(directory):
                    Popen(
                        ["duplicity", "bu", directory, peer],
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                    )
                else:
                    eprint(f"{directory} is not a valid directory.")


def main():
    duper = Duplicity("config.toml")
    duper.dupe_backup()


if __name__ == "__main__" and not sys.flags.interactive:
    main()
