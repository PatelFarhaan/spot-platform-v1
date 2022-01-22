#! /bin/bash

echo_sts() {
  aws sts get-caller-identity
}

activate_virtualenv() {
  echo "$root_path"
}

check_if_platform_is_deployed() {
  cd "$scripts_path" &&
  echo "yet to be completed"
}


root_path=`pwd`
scripts_path="./scripts"


# Copy the entire logic of checking if platform is deployed and pushing the tfstate files back to S3
# Search if you can upload a json text in Jenkins
