#!/bin/bash

set -e -x
s3_spotops_agents_bucket='docker-agents'
s3_app_bucket='redflag-api-lookup-staging'

sudo rm -rf /var/lib/cloud/*

cd /etc/profile.d/
aws s3 cp s3://spot-platform/${s3_app_bucket}/spotops_cloud_init.sh ./
sudo chmod +x ./spotops_cloud_init.sh
source ./spotops_cloud_init.sh

cd /var/opt/spotops/agents
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_ID}
aws s3 cp s3://spot-platform/${s3_app_bucket}/app.env ./
aws s3 cp s3://spot-platform/${s3_app_bucket}/promtail.env ./
aws s3 cp s3://spot-platform/${s3_spotops_agents_bucket}/ ./ --recursive
sudo -E docker-compose up -d --build --force-recreate --remove-orphans