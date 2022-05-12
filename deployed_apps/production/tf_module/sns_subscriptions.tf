// Creating SNS Topic Subscriptions
resource "aws_sns_topic_subscription" "spot_instance_subscriptions" {
  count = length(var.sns_subscriptions_metadata)

  protocol  = var.sns_subscriptions_metadata[count.index]["protocol"]
  endpoint  = var.sns_subscriptions_metadata[count.index]["endpoint"]
  topic_arn = aws_sns_topic.spot_instance_update_sns_topic.arn
}
