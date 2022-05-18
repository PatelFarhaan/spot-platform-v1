// Creating Launch Template for Spot instances
resource "aws_launch_template" "spot_launch_template" {
  update_default_version = true
  ebs_optimized          = false
  image_id               = var.ami_id
  name_prefix            = var.prefix_name
  key_name               = var.ssh_key_name
  vpc_security_group_ids = [aws_security_group.instance_security_group.id]
  user_data              = base64encode(data.template_file.spotops_user_data.rendered)

  monitoring {
    enabled = false
  }

  iam_instance_profile {
    name = var.iam_role
  }

  metadata_options {
    http_endpoint          = "enabled"
    instance_metadata_tags = "enabled"
  }

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_type           = "gp2"
      delete_on_termination = "true"
      volume_size           = var.ebs_volume_size
    }
  }

  lifecycle {
    create_before_destroy = true
  }

  tag_specifications {
    resource_type = "instance"
    tags = var.tags
  }

  tag_specifications {
    resource_type = "volume"
    tags = var.tags
  }
}

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
