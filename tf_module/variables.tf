variable "env" {}

variable "ami_id" {}

variable "vpc_id" {}

variable "tags" {
  type = map(string)
}

variable "app_name" {}

variable "platform" {}

variable "iam_role" {}

variable "aws_region" {}

variable "aws_ecr_acc_id" {}

variable "subnet_ids" {
  type = list(string)
}
variable "prefix_name" {}

variable "ssh_key_name" {}

variable "acm_certificate" {}

variable "ebs_volume_size" {}

variable "alb_security_group" {}

variable "asg_availability_zones" {}

variable "instance_security_group_sg" {}

variable "instance_security_group_cidr" {}

variable "sns_subscriptions_metadata" {
  type = list(map(string))
}

variable "spot_instance_type" {
  type = list(string)
}


variable "spot_asg_min_instances" {}

variable "spot_asg_max_instances" {}

variable "spot_asg_desired_instances" {}


variable "od_instance_type" {}

variable "od_asg_min_instances" {}

variable "od_asg_max_instances" {}

variable "od_asg_desired_instances" {}

