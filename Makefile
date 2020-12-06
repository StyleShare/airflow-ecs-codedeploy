export AWS_DEFAULT_REGION ?= ap-northeast-2
export IMAGE_VERSION ?= $(shell git rev-parse HEAD)

local-compose-up:
	sh scripts/local-compose.sh
local-compose-down:
	sh scripts/local-compose-down.sh
local-docker-build:
	docker build -t airflow-ecs .
staging-ecr-deploy:
	sh scripts/ecr-deploy.sh airflow-v2 staging airflow-ecs
staging-terraform-apply:
	terraform apply --var-file="infrastructure/tfvars/staging.tfvars" -var image_version="$(IMAGE_VERSION)" -auto-approve infrastructure
staging-deploy: local-docker-build staging-ecr-deploy staging-terraform-apply