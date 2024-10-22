#!/bin/bash

# Enable errexit, nounset, and pipefail
set -o errexit -o nounset

exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --no-access-log