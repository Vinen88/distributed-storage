# from rich import print
# from pathlib import Path
import typer

from duplicity import Duplicity
from pathlib import Path

app = typer.Typer()

default_config_path = str((Path(__file__) / ".." / "config.toml").resolve())


@app.command()
def main(
    config: str = typer.Argument(
        default_config_path, help="Path to the TOML config file"
    ),
    verbose: bool = typer.Option(True, help="Enable screamy logging"),
):
    duper = Duplicity(config_filepath=config, verbose=verbose)
    duper.dupe_backup()


if __name__ == "__main__":
    app()
