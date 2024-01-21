# from rich import print
# from pathlib import Path
import typer

from duplicity import Duplicity
from pathlib import Path
from install import create_service

app = typer.Typer()

default_config_path = str((Path(__file__) / ".." / "config.toml").resolve())


SERVICE_NAME = "distributed-storage.service"
SERVICE_PATH = (Path("/etc/systemd/system/") / SERVICE_NAME).resolve()
THIS_DIR = (Path(__file__) / "..").resolve()


@app.command()
def main(
    config: str = typer.Argument(
        default_config_path, help="Path to the TOML config file"
    ),
    verbose: bool = typer.Option(True, help="Enable screamy logging"),
):
    duper = Duplicity(config_filepath=config, verbose=verbose)
    duper.dupe_backup()


@app.command()
def install_client(
    user: str = typer.Option(help="User to run the systemd service as."),
    service_install: Path = typer.Option(
        help="Path to install the systemd service to", default=SERVICE_PATH
    ),
):
    create_service(user, THIS_DIR, service_install)


if __name__ == "__main__":
    app()
