#<==================================================================================================>
#                                            VARIABLES
#<==================================================================================================>
APP ?= api-lookup
ENV ?= staging
AWS_REGION ?= us-east-1
TF_DIR := deployed_apps/$(ENV)/$(APP)/tf_script

#<==================================================================================================>
#                                         TERRAFORM TARGETS
#<==================================================================================================>

.PHONY: init plan apply destroy clean

## Initialize Terraform for a specific app/environment
init:
	cd $(TF_DIR) && terraform init

## Plan Terraform changes
plan:
	cd $(TF_DIR) && terraform plan

## Apply Terraform changes
apply:
	cd $(TF_DIR) && terraform apply

## Destroy Terraform-managed infrastructure
destroy:
	cd $(TF_DIR) && terraform destroy

#<==================================================================================================>
#                                         PACKER TARGETS
#<==================================================================================================>

## Build MCP AMI
build-mcp-ami:
	cd mcp && packer init ami.pkr.hcl && packer build -var 'ami_name=mcp-$(shell date +%Y%m%d)' ami.pkr.hcl

## Build Worker Agent AMI
build-worker-ami:
	cd worker_agents/ami && packer init ami.pkr.hcl && packer build -var 'ami_name=worker-$(shell date +%Y%m%d)' ami.pkr.hcl

#<==================================================================================================>
#                                        DOCKER TARGETS
#<==================================================================================================>

## Start the MCP monitoring stack
docker-up:
	cd mcp/docker_agents && docker-compose up -d

## Stop the MCP monitoring stack
docker-down:
	cd mcp/docker_agents && docker-compose down

## Rebuild and restart the MCP monitoring stack
docker-rebuild:
	cd mcp/docker_agents && docker-compose up -d --build --force-recreate

#<==================================================================================================>
#                                        DEPLOY TARGETS
#<==================================================================================================>

## Deploy app config to S3
deploy-config:
	cd deployed_apps/$(ENV)/$(APP) && bash deploy_config.sh

#<==================================================================================================>
#                                        CLEANUP TARGETS
#<==================================================================================================>

## Clean compiled Python files
clean:
	bash compiled_files_cleanup.sh
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

## Remove all Terraform state and cache files
clean-tf:
	find . -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.tfstate*" -delete 2>/dev/null || true
	find . -name ".terraform.lock.hcl" -delete 2>/dev/null || true

.PHONY: help
help:
	@echo "Usage: make <target> [APP=app-name] [ENV=staging|production]"
	@echo ""
	@echo "Terraform:"
	@echo "  init           Initialize Terraform for APP/ENV"
	@echo "  plan           Plan Terraform changes"
	@echo "  apply          Apply Terraform changes"
	@echo "  destroy        Destroy infrastructure"
	@echo ""
	@echo "Packer:"
	@echo "  build-mcp-ami     Build MCP monitoring AMI"
	@echo "  build-worker-ami  Build worker agent AMI"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up         Start MCP monitoring stack"
	@echo "  docker-down       Stop MCP monitoring stack"
	@echo "  docker-rebuild    Rebuild MCP monitoring stack"
	@echo ""
	@echo "Other:"
	@echo "  deploy-config     Deploy app config to S3"
	@echo "  clean             Clean compiled files"
	@echo "  clean-tf          Remove Terraform state files"
