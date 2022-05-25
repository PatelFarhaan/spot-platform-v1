// Create an application load balancer
resource "aws_alb" "load_balancer" {
  idle_timeout               = 3600
  internal                   = false
  enable_deletion_protection = false
  load_balancer_type         = "application"
  subnets                    = var.subnet_ids
  name_prefix                = var.prefix_name
  security_groups            = [aws_security_group.alb_security_group.id]

  tags = merge(var.tags, {
    Name = "alb-tf"
  })
}


// Create the LB security group
resource "aws_security_group" "alb_security_group" {
  vpc_id      = var.vpc_id
  name        = "${var.app_name}-${var.env}-alb-tf"
  description = "Allow all inbound traffic on port 80 and 443"

  dynamic "ingress" {
    for_each = var.alb_security_group

    content {
      to_port     = lookup(ingress.value, "to_port")
      protocol    = lookup(ingress.value, "protocol")
      from_port   = lookup(ingress.value, "from_port")
      description = lookup(ingress.value, "description")
      cidr_blocks = lookup(ingress.value, "cidr_blocks")
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.app_name}-alb-tf"
  })
}


// Create the instance security group
resource "aws_security_group" "instance_security_group" {
  vpc_id      = var.vpc_id
  description = "Allow all traffic from load balancer"
  name        = "${var.app_name}-${var.env}-instance-tf"

  dynamic "ingress" {
    for_each = var.instance_security_group_cidr

    content {
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      from_port   = ingress.value.from_port
      description = ingress.value.description
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  dynamic "ingress" {
    for_each = var.instance_security_group_sg

    content {
      to_port         = ingress.value.to_port
      protocol        = ingress.value.protocol
      from_port       = ingress.value.from_port
      description     = ingress.value.description
      security_groups = ingress.value.security_groups
    }
  }

  ingress {
    description     = "Traffic from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.app_name}-instance-tf"
  })
}


// Creating LB listeners on port 80
resource "aws_alb_listener" "alb_listeners_port_80" {
  port              = "80"
  protocol          = "HTTP"
  load_balancer_arn = aws_alb.load_balancer.arn

  #  default_action {
  #    type = "redirect"
  #
  #    redirect {
  #      port        = "443"
  #      protocol    = "HTTPS"
  #      status_code = "HTTP_301"
  #    }
  #  }

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.alb_target_group.arn
  }

  tags = merge(var.tags, {
    Name = "alb-listeners-port-80-tf"
  })
}


// Creating LB listeners on port 443
resource "aws_alb_listener" "alb_listeners_port_443" {
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn   = var.acm_certificate
  load_balancer_arn = aws_alb.load_balancer.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.alb_target_group.arn
  }

  tags = merge(var.tags, {
    Name = "alb-listeners-port-443-tf"
  })
}
