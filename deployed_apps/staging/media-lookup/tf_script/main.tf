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
module "app-spot-platform" {
  source = "./../../../../tf_module"

  env                        = local.config_data.env
  tags                       = local.config_data.tags
  ami_id                     = local.config_data.ami_id
  vpc_id                     = local.config_data.vpc_id
  app_name                   = local.config_data.app_name
  platform                   = local.config_data.platform
  iam_role                   = local.config_data.iam_role
  subnet_ids                 = local.config_data.subnet_ids
  aws_region                 = local.config_data.aws_region
  prefix_name                = local.config_data.prefix_name
  ssh_key_name               = local.config_data.ssh_key_name
  aws_ecr_acc_id             = local.config_data.aws_ecr_acc_id
  ebs_volume_size            = local.config_data.ebs_volume_size
  acm_certificate            = local.config_data.acm_certificate
  asg_availability_zones     = local.config_data.availability_zones
  sns_subscriptions_metadata = local.config_data.sns_subscriptions_metadata
  alb_security_group         = local.config_data.security_groups.alb.ingress
  instance_security_group_sg   = local.config_data.security_groups.instance.ingress.sg
  instance_security_group_cidr = local.config_data.security_groups.instance.ingress.cidr

  od_instance_type         = local.config_data.od_config.instance_type
  od_asg_min_instances     = local.config_data.od_config.auto_scaling_group.min_instances
  od_asg_max_instances     = local.config_data.od_config.auto_scaling_group.max_instances
  od_asg_desired_instances = local.config_data.od_config.auto_scaling_group.desired_instances

  spot_instance_type         = local.config_data.spot_config.instance_type
  spot_asg_min_instances     = local.config_data.spot_config.auto_scaling_group.min_instances
  spot_asg_max_instances     = local.config_data.spot_config.auto_scaling_group.max_instances
  spot_asg_desired_instances = local.config_data.spot_config.auto_scaling_group.desired_instances
}
