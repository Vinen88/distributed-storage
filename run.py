# from rich import print
# from pathlib import Path
import typer

from duplicity import Duplicity
from pathlib import Path
from install import create_service

app = typer.Typer()

default_config_path = str((Path(__file__) / ".." / "config.toml").resolve())


SERVICE_NAME_CLIENT = "distributed-storage-client.service"
SERVICE_PATH_CLIENT = (Path("/etc/systemd/system/") / SERVICE_NAME_CLIENT).resolve()
SERVICE_NAME_SERVER = "distributed-storage-server.service"
SERVICE_PATH_SERVER = (Path("/etc/systemd/system/") / SERVICE_NAME_SERVER).resolve()
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
    user: str = typer.Option(help="User to run the systemd service as.", default="root"),
    service_install: Path = typer.Option(
        help="Path to install the systemd service to", default=SERVICE_PATH_CLIENT
    ),
):
    create_service(user, THIS_DIR, service_install, "run_in_venv.bash")

@app.command()
def install_server(
    user: str = typer.Option(help="User to run the systemd service as.", default="root"),
    service_install: Path = typer.Option(
        help="Path to install the systemd service to", default=SERVICE_PATH_SERVER        
    ),
    share_folder: Path = typer.Option(
        help="Folder for the server to backup"
    )
):
    share_folder = str(share_folder.resolve())
    create_service(user, THIS_DIR / "server", service_install, f"start_server.bash '{share_folder}'")




if __name__ == "__main__":
    app()
