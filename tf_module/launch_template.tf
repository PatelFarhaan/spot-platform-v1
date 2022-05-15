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

sudo rm -rf /var/lib/cloud/*
sleep 10

cd /etc/profile.d/
aws s3 cp s3://spot-platform/$s3_app_bucket/spotops_cloud_init.sh ./
sudo chmod +x ./spotops_cloud_init.sh
source ./spotops_cloud_init.sh

cd /var/opt/spotops/agents
sleep 10
aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${var.aws_ecr_acc_id}
aws s3 cp s3://spot-platform/$s3_app_bucket/app.env ./
aws s3 cp s3://spot-platform/$s3_app_bucket/promtail.env ./
aws s3 cp s3://spot-platform/$s3_spotops_agents_bucket/ ./ --recursive
python3 create_nginx_conf.py

sleep 10
sudo -E docker-compose up -d --build --force-recreate --remove-orphans
EOF
}
