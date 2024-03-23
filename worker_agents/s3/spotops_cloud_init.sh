#!/bin/bash

set -e -x
export HOSTNAME=`hostname`
no_of_cores=`nproc --all`
APP_REPLICAS=$(( ($no_of_cores * 2) + 1 ))
export APP_REPLICAS=$APP_REPLICAS
