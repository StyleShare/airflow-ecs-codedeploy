#!/usr/bin/env bash

PROJECT_NAME=$1
STAGE_NAME=$2
LOCAL_IMAGE_NAME=$3
REPOSITORY_NAME=$PROJECT_NAME-$STAGE_NAME

aws ecr get-login-password --region "$AWS_DEFAULT_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT".dkr.ecr."$AWS_DEFAULT_REGION".amazonaws.com

docker tag "$LOCAL_IMAGE_NAME":latest "$AWS_ACCOUNT".dkr.ecr."$AWS_DEFAULT_REGION".amazonaws.com/"$REPOSITORY_NAME":latest
docker push "$AWS_ACCOUNT".dkr.ecr."$AWS_DEFAULT_REGION".amazonaws.com/"$REPOSITORY_NAME":latest

COMMIT_SHA=$(git rev-parse HEAD)
docker tag "$LOCAL_IMAGE_NAME":latest "$AWS_ACCOUNT".dkr.ecr."$AWS_DEFAULT_REGION".amazonaws.com/"$REPOSITORY_NAME":"$COMMIT_SHA"
docker push "$AWS_ACCOUNT".dkr.ecr."$AWS_DEFAULT_REGION".amazonaws.com/"$REPOSITORY_NAME":"$COMMIT_SHA"
