python commands/write_env_file_command_line.py "$ENV_PATH"

python commands/upload_env_to_s3_command_line.py \
  --bucket_name "$BUCKET_NAME" \
  --key_name "$KEY_NAME" \
  "$ENV_PATH"
