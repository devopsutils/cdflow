#!/bin/bash

set -euo pipefail

IMAGE_ID="$(basename $(pwd))-release"

docker image build -t "${IMAGE_ID}" .

docker container run --rm --name "${IMAGE_ID}" \
    -i $(tty -s && echo -t) \
    -e GITHUB_TOKEN \
    "${IMAGE_ID}" \
    python release.py "${@}"