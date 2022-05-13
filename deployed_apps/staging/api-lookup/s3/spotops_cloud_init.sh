#!/bin/bash

no_of_cores=`nproc --all`
APP_REPLICAS=$(( ($no_of_cores * 2) + 1 ))
export APP_REPLICAS=$APP_REPLICAS

export HOSTNAME=`hostname`
export CLIENT_APP_PORT=5000
export CLIENT_APP_IMAGE="${AWS_ECR_ID}/redflag-api-lookup:staging-1"