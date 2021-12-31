variable "env" {}

variable "ami_id" {}

variable "vpc_id" {}

variable "tags" {
  type = map(string)
}

variable "aws_region" {}

variable "subnet_ids" {
  type = list(string)
}

variable "acm_certificate" {}

variable "asg_min_instances" {}

variable "asg_max_instances" {}

variable "spot_instance_type" {}

variable "spot_instance_price" {}

variable "asg_desired_instances" {}

variable "launch_config_key_name" {}

variable "asg_availability_zones" {}
