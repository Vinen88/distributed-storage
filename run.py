# from rich import print
# from pathlib import Path
import typer

from duplicity import Duplicity


app = typer.Typer()


@app.command()
def main(
    config: str = typer.Argument(None, help="Path to the TOML config file"),
    verbose: bool = typer.Option(False, help="Enable screamy logging"),
):
    duper = Duplicity(config)
    duper.dupe_backup()


if __name__ == "__main__":
    app()
