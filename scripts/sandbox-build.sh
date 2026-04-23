#!/usr/bin/env bash

set -euo pipefail

docker build -t sandbox-runner:latest -f infra/sandbox/Dockerfile .
