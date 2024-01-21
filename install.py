import toml
from pathlib import Path
import os


def create_service(user: str, cwd: Path, service_install: Path):
    "creates a service"

    text = (
        toml.dumps(
            {
                "Unit": {
                    "Description": "Duplicity backup service",
                },
                "Service": {
                    "User": user,
                    "WorkingDirectory": str(cwd),
                    "ExecStart": f"{cwd/'run_in_venv.bash'}",
                },
                "Install": {
                    "WantedBy": "multi-user.target",
                },
            },
        )
        .replace('"', "")
        .replace(" = ", "=")
    )
    with open(service_install, "wt", encoding="utf-8") as fo:
        fo.write(text)
    os.system(f'systemctl enable "{str(service_install)}"')
    os.system(f'systemctl start "{str(service_install)}"')
