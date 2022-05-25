// User data for Spot and OD
data "template_file" "spotops_user_data" {
  template = <<EOF
#!/bin/bash

set -e -x
pip3 install python-nginx
export AWS_ECR_ID=${var.aws_ecr_acc_id}
s3_spotops_agents_bucket='docker-agents'
s3_app_bucket='${var.env}/${var.app_name}'
s3_bucket_mount=spot-platform:/$s3_app_bucket

sudo rm -rf /var/lib/cloud/*
cd /var/opt/spotops/agents
sudo chown ubuntu:ubuntu -R /var/opt/spotops/agents/
mkdir app_config s3_cache

sudo s3fs -o iam_role='${var.iam_role}' -o use_cache=./s3_cache $s3_bucket_mount app_config
sudo cp ./app_config/deployment.sh /etc/profile.d/
sudo chown ubuntu:ubuntu /etc/profile.d/deployment.sh
sudo chmod +x /etc/profile.d/deployment.sh
source /etc/profile.d/deployment.sh
source /etc/profile.d/spotops_cloud_init.sh

sleep 10
aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${var.aws_ecr_acc_id} &&
aws s3 cp s3://spot-platform/$s3_spotops_agents_bucket/ ./ --exclude 'excludes/*' --recursive
python3 create_nginx_conf.py

sleep 10
sudo -E docker-compose up -d --build --force-recreate --remove-orphans
EOF
}