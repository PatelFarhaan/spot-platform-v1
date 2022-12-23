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
module "main-control-plane" {
  source = "."

  env            = local.config_data.env
  tags           = local.config_data.tags
  aws_region     = local.config_data.aws_region
  subnet_id      = local.config_data.subnet_id
  iam_profile    = local.config_data.iam_profile
  volume_size    = local.config_data.volume_size
  company_name   = local.config_data.company_name
  instance_size  = local.config_data.instance_size
  key_name_pair  = local.config_data.key_name_pair
  security_group = local.config_data.security_group
}
