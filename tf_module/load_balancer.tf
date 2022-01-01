// Create an application load balancer
resource "aws_alb" "gitlab_load_balancer" {
  idle_timeout               = 3600
  internal                   = false
  load_balancer_type         = "application"
  enable_deletion_protection = false
  subnets                    = var.subnet_ids
  name                       = "gitlab-runner-alb-tf"
  security_groups            = [aws_security_group.gitlab_alb_security_group.id]

  tags = merge(var.tags, {
    Name = "gitlab-runner-alb-tf"
  })
}


// Create the LB security group
resource "aws_security_group" "gitlab_alb_security_group" {
  vpc_id      = var.vpc_id
  name        = "gitlab-alb-security-group-tf"
  description = "Allow all inbound traffic on port 80 and 443"

  ingress {
    description      = "HTTP from VPC"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "TLS from VPC"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(var.tags, {
    Name = "gitlab-alb-security-group-tf"
  })
}


// Create the instance security group
resource "aws_security_group" "gitlab_instance_security_group" {
  vpc_id      = var.vpc_id
  name        = "gitlab-instance-security-group-tf"
  description = "Allow all traffic from load balancer"

  ingress {
    description     = "HTTP"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.gitlab_alb_security_group.id]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(var.tags, {
    Name = "gitlab-instance-security-group-tf"
  })
}


// Creating the target group
resource "aws_alb_target_group" "gitlab_alb_target_group" {
  port        = 80
  protocol    = "HTTP"
  name_prefix = "gl-tf-"
  vpc_id      = var.vpc_id
  deregistration_delay = 60

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(var.tags, {
    Name = "gitlab-target-group-tf"
  })
}


// Creating LB listeners on port 80
resource "aws_alb_listener" "gitlab_alb_listeners_port_80" {
  port              = "80"
  protocol          = "HTTP"
  load_balancer_arn = aws_alb.gitlab_load_balancer.arn

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }

  tags = merge(var.tags, {
    Name = "gitlab-alb-listeners-port-80-tf"
  })
}


// Creating LB listeners on port 443
resource "aws_alb_listener" "gitlab_alb_listeners_port_443" {
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn   = var.acm_certificate
  load_balancer_arn = aws_alb.gitlab_load_balancer.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.gitlab_alb_target_group.arn
  }

  tags = merge(var.tags, {
    Name = "gitlab-alb-listeners-port-443-tf"
  })
}
