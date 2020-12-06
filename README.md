# Container Based Airflow Development Lifecycle 

## Requirements

- AWS IAM 
    - S3 Read
    - S3 Write (optional)
    - ECS Full (optional)
    - ECR Full (optional)
    - ElasticCache Full (optional)
    
- Set environment variables
```
export AWS_ACCOUNT=123456789
export AWS_DEFAULT_REGION=ap-northeast-2-or-something-else
export AWS_ACCESS_KEY_ID=123456789
export AWS_SECRET_ACCESS_KEY=123456789
```
- Docker 
- Docker Compose
- Python 3.8.2

# Local Environment
```
user >> shell script >> env from s3 (KMS Encrypted) >> docker-compose >> app start
```

1. Local env upload to s3
```shell script
python commands/write_env_file_command_line.py "$ENV_PATH"
```
Python Click으로 만들어진 CLI로 envfile을 작성하고, $ENV_PATH에 dotenv 파일을 만듭니다.  

```shell script
python commands/upload_env_to_s3_command_line.py \
  --bucket_name "$BUCKET_NAME" \
  --key_name "$KEY_NAME" \
  "$ENV_PATH"
```
$ENV_PATH의 dotenv 파일을 s3의 특정 위치에 업로드합니다. (기본 KMS 암호화)

or just run
```shell script
sh scripts/update_env.sh $BUCKET_NAME $KEY_NAME $ENV_PATH
```

2. Pull Environment Variables on docker-compose runtime
```shell script
sh scripts/local-compose.sh $BUCKET_NAME $KEY_NAME $ENV_FILE
```


# Staging Environment
```
[master-push] user >> docker build >> ECR push >> ecs update staging cluster (terraform)
```

# Production Environment
```
[release-branch push] >> docker build >> ECR push >> ecs update production cluster (terraform
```