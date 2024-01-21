#!/usr/bin/env bash
# Usage: ./start_server.bash <directory>

DIRECTORY="$1"

# https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

pushd "$SCRIPT_DIR"
    docker build -t distributed-storage-server .
    docker run --rm --net host -v "$DIRECTORY":/www distributed-storage-server
popd
