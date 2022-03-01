#! /bin/bash


current_path=`pwd` &&
cd "tf_script" &&
terraform validate &&
terraform apply -auto-approve &&
cd "$current_path" &&
cd "./../../../../../scripts/jenkins_automation/" &&
bash create_asg_job.sh
