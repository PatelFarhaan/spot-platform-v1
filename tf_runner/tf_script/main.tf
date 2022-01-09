// Defining TF module provider
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
  source = "./../../tf_module"

  env                         = local.config_data.env
  tags                        = local.config_data.tags
  ami_id                      = local.config_data.ami_id
  vpc_id                      = local.config_data.vpc_id
  app_name                    = local.config_data.app_name
  subnet_ids                  = local.config_data.subnet_ids
  aws_region                  = local.config_data.aws_region
  ssh_key_name                = local.config_data.ssh_key_name
  acm_certificate             = local.config_data.acm_certificate
  spot_instance_type          = local.config_data.spot_config.instance_type
  spot_instance_price         = local.config_data.spot_config.instance_price
  spot_ebs_volume_size        = local.config_data.spot_config.ebs_volume_size
  spot_asg_min_instances      = local.config_data.spot_config.auto_scaling_group.min_instances
  spot_asg_max_instances      = local.config_data.spot_config.auto_scaling_group.max_instances
  spot_asg_desired_instances  = local.config_data.spot_config.auto_scaling_group.desired_instances
  spot_asg_availability_zones = local.config_data.spot_config.auto_scaling_group.availability_zones
}
