// Creating the ASG Policies for Spot instances
resource "aws_autoscaling_policy" "spot_asg_policies" {
  name = "spot-${var.app_name}"
  autoscaling_group_name = aws_autoscaling_group.on_demand_autoscaling_group

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }

    target_value = 30.0
  }
}


// Creating the ASG Policies for OD instances
resource "aws_autoscaling_policy" "od_asg_policies" {
  name = "od-${var.app_name}"
  autoscaling_group_name = aws_autoscaling_group.on_demand_autoscaling_group

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }

    target_value = 30.0
  }
}