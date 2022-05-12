#!/bin/bash

app_name=`cat config.json | jq -r .app_name`
env=`cat config.json | jq -r .env`
s3_app_bucket="${env}/${app_name}"
echo "Deploying config to: ${s3_app_bucket}..."
echo "" 
cd ./s3 &&
aws s3 cp ./ "s3://spot-platform/${s3_app_bucket}/" --recursive