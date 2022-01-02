terraform {
  required_providers {
    aws      = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    template = {
      version = "2.2.0"
    }
  }
}


// Reading data variables from app_config.json file
locals {
  config_data = jsondecode(file("./../config.json"))
}


// Using pre-declared module
module "gitlab-runners-dev-us-east-1" {
  source = "./../../../../tf_module"

  env                    = local.config_data.env
  tags                   = local.config_data.tags
  ami_id                 = local.config_data.ami_id
  vpc_id                 = local.config_data.vpc_id
  subnet_ids             = local.config_data.subnet_ids
  aws_region             = local.config_data.aws_region
  acm_certificate        = local.config_data.acm_certificate
  spot_instance_type     = local.config_data.spot_instance_type
  spot_instance_price    = local.config_data.spot_instance_price
  launch_config_key_name = local.config_data.launch_config_key_name
  asg_min_instances      = local.config_data.auto_scaling_group.min_instances
  asg_max_instances      = local.config_data.auto_scaling_group.max_instances
  asg_desired_instances  = local.config_data.auto_scaling_group.desired_instances
  asg_availability_zones = local.config_data.auto_scaling_group.availability_zones
}
