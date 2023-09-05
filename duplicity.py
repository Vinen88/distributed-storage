import os
import sys
from operator import itemgetter
from subprocess import Popen, PIPE
from dotenv import load_dotenv
import tomllib
from typing import Union, Literal
from itertools import product
from functools import partial

load_dotenv()

Config = dict[Union[Literal["peers"], Literal["backup"]]]
eprint = partial(print, file=sys.stderr)


class Duplicity:
    def __init__(self, filepath: str) -> None:
        self.config_date = None
        self.config = None
        self.filepath = filepath
        self.load_config()
        self.peers = Duplicity.get_some(self.config["peers"], "url")
        self.dirs = Duplicity.get_some(self.config["backups"], "dir")

    def load_config(self) -> Config:
        changed = self.config_date != os.path.getmtime(self.filepath)
        if self.config is not None and changed:
            return
        with open(self.filepath, "rb") as fo:
            self.config = tomllib.load(fo)
        self.config_date = os.path.getmtime(self.filepath)

    @staticmethod
    def get_some(config: dict, key: str) -> list:
        return tuple(map(itemgetter(key), config))

    def dupe_backup(self) -> None:
        self.load_config()
        for peer, directory in product(self.peers, self.dirs):
            if not os.path.isdir(directory):
                eprint(f"{directory} is not a valid directory.")
                continue
            eprint(f'duping: "{directory}" TO "{peer}"')
            Popen(
                ["duplicity", "bu", directory, peer],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
            )


def main():
    duper = Duplicity("config.toml")
    duper.dupe_backup()


if __name__ == "__main__" and not sys.flags.interactive:
    main()
