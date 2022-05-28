#!/bin/bash

no_of_cores=`nproc --all`
APP_REPLICAS=$(( ($no_of_cores * 2) + 1 ))
export APP_REPLICAS=$APP_REPLICAS

export HOSTNAME=`curl http://169.254.169.254/latest/meta-data/instance-id`