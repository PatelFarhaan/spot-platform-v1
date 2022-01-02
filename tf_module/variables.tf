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
variable "ssh_key_name" {}

variable "acm_certificate" {}

variable "spot_instance_type" {}

variable "spot_instance_price" {}

variable "spot_ebs_volume_size" {}

variable "spot_asg_min_instances" {}

variable "spot_asg_max_instances" {}

variable "spot_asg_desired_instances" {}

variable "spot_asg_availability_zones" {}
