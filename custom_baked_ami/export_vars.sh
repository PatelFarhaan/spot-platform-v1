no_of_cores=`nproc --all`
APP_REPLICAS=$(( ($no_of_cores * 2) + 1 ))
export APP_REPLICAS=$APP_REPLICAS
export HOSTNAME=${HOSTNAME}