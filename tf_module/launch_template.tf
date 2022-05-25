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
