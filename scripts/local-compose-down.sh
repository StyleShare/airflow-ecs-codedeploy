#!/bin/bash
set -euo pipefail

BUCKET_NAME=$1
KEY_NAME=$2
ENV_FILE=$3

eval "$(python commands/load_env_file_from_s3_command_line.py -b "$BUCKET_NAME" -k "$KEY_NAME" "$ENV_FILE")" \
  docker-compose down -v
