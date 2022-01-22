// Creating the ASG for Spot instances
resource "aws_autoscaling_group" "spot_autoscaling_group" {
  vpc_zone_identifier  = var.subnet_ids
  name_prefix          = var.prefix_name
  min_size             = var.spot_asg_min_instances
  max_size             = var.spot_asg_max_instances
  termination_policies = ["ClosestToNextInstanceHour"]
  desired_capacity     = var.spot_asg_desired_instances
  target_group_arns    = [aws_alb_target_group.alb_target_group.arn]

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 0
      on_demand_percentage_above_base_capacity = 0
      spot_allocation_strategy                 = "capacity-optimized"
    }

    launch_template {
      launch_template_specification {
        version            = "$Latest"
        launch_template_id = aws_launch_template.spot_launch_template.id
      }

      # Todo: Add a for loop for spot instances

      override {
        instance_type = "r5.2xlarge"
      }

      override {
        instance_type = "r5a.2xlarge"
      }

      override {
        instance_type = "r5b.2xlarge"
      }

      override {
        instance_type = "r5n.2xlarge"
      }

      override {
        instance_type = "r6g.2xlarge"
      }

      override {
        instance_type = "r6i.2xlarge"
      }

    }
  }

  health_check_grace_period = 30
  default_cooldown          = 15
  capacity_rebalance        = true
  health_check_type         = "EC2"

  instance_refresh {
    triggers = ["tag"]
    strategy = "Rolling"
    preferences {
      checkpoint_delay       = 15
      min_healthy_percentage = 90
    }
  }

  tags = concat([
  for key, value in var.tags : {
    key                 = key
    value               = value
    propagate_at_launch = true
  }
  ], [
    {
      key                 = "Name"
      value               = "spot-${var.app_name}"
      propagate_at_launch = true
    }
  ])
}
