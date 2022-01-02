// Creating Launch Config
resource "aws_launch_configuration" "gitlab_launch_configuration" {
  image_id        = var.ami_id
  key_name        = var.ssh_key_name
  name_prefix     = "${var.app_name}-"
  instance_type   = var.spot_instance_type
  spot_price      = var.spot_instance_price
  security_groups = [aws_security_group.gitlab_instance_security_group.id]

  root_block_device {
    delete_on_termination = true
    volume_size           = var.spot_ebs_volume_size
  }

  lifecycle {
    create_before_destroy = true
  }
}


// Creating the ASG
resource "aws_autoscaling_group" "gitlab_autoscaling_group" {
  vpc_zone_identifier  = var.subnet_ids
  name_prefix          = "${var.app_name}-"
  min_size             = var.spot_asg_min_instances
  max_size             = var.spot_asg_max_instances
  termination_policies = ["ClosestToNextInstanceHour"]
  desired_capacity     = var.spot_asg_desired_instances
  target_group_arns    = [aws_alb_target_group.gitlab_alb_target_group.arn]
  launch_configuration = aws_launch_configuration.gitlab_launch_configuration.name

  health_check_grace_period = 30
  default_cooldown          = 15
  capacity_rebalance        = true
  health_check_type         = "EC2"

  instance_refresh {
    strategy = "Rolling"
    preferences {
      checkpoint_delay       = 15
      min_healthy_percentage = 90
    }
  }

  tags = [
  for key, value in var.tags : {
    key                 = key
    value               = value
    propagate_at_launch = true

  }
  ]
}
