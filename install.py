import toml
from pathlib import Path
import os


def create_service(user: str, cwd: Path, service_install: Path, exec_start: str):
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
                    "ExecStart": f"{str((cwd/exec_start).resolve())}",
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
    
    os.system(f'systemctl enable "{service_install.name}"')
    os.system(f'systemctl start "{service_install.name}"')
