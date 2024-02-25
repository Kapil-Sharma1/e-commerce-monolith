#! /bin/bash

set -o allexport
source .env
set +o allexport

celery -A config --workdir="./backend/" worker -c 4 --loglevel=DEBUG
