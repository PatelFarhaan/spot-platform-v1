// Creating the ASG for Spot instances
resource "aws_autoscaling_group" "spot_autoscaling_group" {
  vpc_zone_identifier  = var.subnet_ids
  name_prefix          = var.prefix_name
  termination_policies = ["OldestInstance"]
  min_size             = var.spot_asg_min_instances
  max_size             = var.spot_asg_max_instances
  desired_capacity     = var.spot_asg_desired_instances
  target_group_arns    = [aws_alb_target_group.alb_target_group.arn]

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 0
      on_demand_percentage_above_base_capacity = 0
      spot_allocation_strategy                 = "lowest-price"
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.spot_launch_template.id
        version            = aws_launch_template.spot_launch_template.latest_version
      }

      dynamic override {
        for_each = var.spot_instance_type
        content {
          instance_type = override.value
        }
      }

    }
  }

  default_cooldown          = 15
  health_check_grace_period = 120
  capacity_rebalance        = true
  health_check_type         = "ELB"

  lifecycle {
    create_before_destroy = true
  }

  instance_refresh {
    triggers = ["tag"]
    strategy = "Rolling"
    preferences {
      checkpoint_delay       = 15
      min_healthy_percentage = 90
    }
  }

  tags = concat(
    [
    for key, value in var.tags :
    {
      key                 = key
      value               = value
      propagate_at_launch = true
    }
    if key != "Name"
    ],
    [
      {
        key                 = "Type"
        value               = "Spot"
        propagate_at_launch = true
      },
      {
        key                 = "Name"
        value               = "${var.platform}-spot-${var.app_name}"
        propagate_at_launch = true
      }
    ]
  )
}