#! /bin/bash


current_path=`pwd` &&
echo "#! /bin/bash" > env.sh
cd "/Users/personal/Projects/spot_platform/tf_runner/redflag/dev/us-east-1/service-lookup/tf_script" &&
terraform output -json | jq ".outputs.value" | jq -r "to_entries|map(\"export \(.key)=\(.value|tostring)\")|.[]" >> "${current_path}/env.sh"
source "${current_path}/env.sh"