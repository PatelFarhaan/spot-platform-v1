#!/bin/bash

s3_bucket="s3://spot-platform/docker-agents/"
echo "Deploying files to: ${s3_bucket}..."
echo ""
cd ./s3 &&
aws s3 cp ./ ${s3_bucket} --recursive
