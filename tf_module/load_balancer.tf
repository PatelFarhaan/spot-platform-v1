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
  name        = "alb-security-group-tf"
  description = "Allow all inbound traffic on port 80 and 443"

  ingress {
    description = "HTTP from VPC"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "alb-security-group-tf"
  })
}


// Create the instance security group
resource "aws_security_group" "instance_security_group" {
  vpc_id      = var.vpc_id
  name        = "instance-security-group-tf"
  description = "Allow all traffic from load balancer"

  ingress {
    description     = "HTTP"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_security_group.id]
  }

  ingress {
    description = "Node Exporter"
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Cadvisor"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Open to world"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "instance-security-group-tf"
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
