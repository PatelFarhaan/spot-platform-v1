// Creating the target group
resource "aws_alb_target_group" "alb_target_group" {
  deregistration_delay = 10
  port                 = 80
  protocol             = "HTTP"
  vpc_id               = var.vpc_id
  name_prefix          = var.prefix_name

  lifecycle {
    create_before_destroy = true
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 120
    interval            = 300
    enabled             = true
    protocol            = "HTTP"
    path                = "/ping"
    matcher             = "200,403,404"
    port                = "traffic-port"
  }

  tags = merge(var.tags, {
    Name = "target-group-tf"
  })
}