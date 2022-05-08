#!/bin/bash

set -e -x
no_of_cores=`nproc --all`
APP_REPLICAS=$(( ($no_of_cores * 2) + 1 ))
export APP_REPLICAS=$APP_REPLICAS

export HOSTNAME=`hostname`
export CLIENT_APP_PORT=5000
export AWS_REGION='us-east-1'
export AWS_ECR_ID='***REMOVED***.dkr.ecr.us-east-1.amazonaws.com'
export CLIENT_APP_IMAGE="${AWS_ECR_ID}/redflag-api-lookup:development-242"
