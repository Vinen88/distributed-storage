import os
import sys
import toml
from subprocess import Popen, PIPE
from dotenv import load_dotenv
from typing import Union, Literal
from itertools import product

load_dotenv()

Config = dict[Union[Literal["peers"], Literal["backup"]]]


class Duplicity:
    def __init__(self, config_filepath: str, verbose=False) -> None:
        self.verbose = verbose
        self.config = None
        self.filepath = config_filepath
        self.load_config()
        self.peers = tuple(peer["url"] for peer in self.config["peers"])
        self.dirs = tuple(backup["dir"] for backup in self.config["backups"])

    def load_config(self) -> Config:
        with open(self.filepath, "rt") as fo:
            self.config = toml.load(fo)
        self.vlog(f"Loaded config file from {self.filepath}")
        self.vlog(str(self.config))

    def dupe_backup(self) -> None:
        self.load_config()
        for peer, directory in product(self.peers, self.dirs):
            if not os.path.isdir(directory):
                self.vlog(f"{directory} is not a valid directory.")
                continue
            self.vlog(f'duping: "{directory}" TO "{peer}"')
            Popen(
                ["duplicity", "bu", directory, peer],
                stdin=PIPE,
                stdout=sys.stderr,
                stderr=sys.stderr,
            )

    def vlog(self, *args, **kwargs):
        if self.verbose:
            print(*args, file=sys.stderr, **kwargs)


def main():
    duper = Duplicity("config.toml")
    duper.dupe_backup()


if __name__ == "__main__" and not sys.flags.interactive:
    main()
