// Creating Cloudwatch rule to capture spot instance updates
resource "aws_cloudwatch_event_rule" "capture_spot_instance_modification" {
  name        = "spot-instance-update-${var.app_name}"
  description = "Rule to capture spot instance updates"

  event_pattern = <<EOF
{
  "source": [
    "aws.autoscaling"
  ],
  "detail-type": [
    "EC2 Instance Launch Successful",
    "EC2 Instance Terminate Successful"
  ],
  "detail": {
    "AutoScalingGroupName": [
      "${aws_autoscaling_group.spot_autoscaling_group.name}"
    ]
  }
}
EOF

  tags = var.tags
}


// Creating cloudwatch rules to send event details to SNS
resource "aws_cloudwatch_event_target" "send_cw_event_to_sns" {
  target_id = "SendToSNS"
  arn       = aws_sns_topic.spot_instance_update_sns_topic.arn
  rule      = aws_cloudwatch_event_rule.capture_spot_instance_modification.name
}
