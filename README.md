# distributed-storage

A system for sharing storage resources amongst trusted individuals to create encrypted backups

## Requirements
- Python 3.X with requirements.txt pip installed
- systemd/docker

## Overview

### Client
- run.py: a simple CLI built with Typer to facilitate automatic backups with the Server 
    - Program also comes with tools to install systemd units for Client & Server
    - Takes config.toml to specify peers and folders for backup
      - Note: this file is reloaded before every backup
    - See run.py --help for more info
### Server
- A simple nginx webdav server for handling backup uploading/downloading
- No auth, must be run behind a VPN
- Server is containerized and can be run using `start_server.bash`
