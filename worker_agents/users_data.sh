#!/bin/bash

set -e -x
sudo rm -rf /var/lib/cloud/*
cd /etc/profile.d/
aws s3 cp s3://spot-platform/redflag-api-lookup-staging/spotops_cloud_init.sh ./
sudo chmod +x ./spotops_cloud_init.sh
source spotops_cloud_init.sh

cd /var/opt/spotops/agents
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ***REMOVED***.dkr.ecr.us-east-1.amazonaws.com
aws s3 cp s3://spot-platform/redflag-api-lookup-staging/app.env
sudo docker-compose up -d --build --force-recreate --remove-orphans