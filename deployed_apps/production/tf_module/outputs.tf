output "spot_asg_name" {
  value = aws_autoscaling_group.spot_autoscaling_group.name
}

output "od_asg_name" {
  value = aws_autoscaling_group.on_demand_autoscaling_group.name
}

output "load_balancer" {
  value = aws_alb.load_balancer.dns_name
}