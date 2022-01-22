variable "env" {}

variable "ami_id" {}

variable "vpc_id" {}

variable "tags" {
  type = map(string)
}

variable "app_name" {}


variable "aws_region" {}


variable "subnet_ids" {
  type = list(string)
}
variable "prefix_name" {}

variable "ssh_key_name" {}

variable "acm_certificate" {}

variable "ebs_volume_size" {}

variable "asg_availability_zones" {}

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
