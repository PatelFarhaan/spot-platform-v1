// Creating notification for Spot ASG
resource "aws_autoscaling_notification" "spot_asg_notification" {
  topic_arn   = aws_sns_topic.spot_instance_update_sns_topic.arn

  group_names = [
    aws_autoscaling_group.spot_autoscaling_group.name,
    aws_autoscaling_group.on_demand_autoscaling_group.name
  ]

  notifications = [
    "autoscaling:EC2_INSTANCE_LAUNCH",
    "autoscaling:EC2_INSTANCE_TERMINATE",
  ]
}