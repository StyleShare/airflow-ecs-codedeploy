#!/bin/bash
set -euo pipefail

eval "$(python commands/load_env_file_from_s3_command_line.py -b "$BUCKET_NAME" -k "$KEY_NAME")" \
  docker-compose down -v
