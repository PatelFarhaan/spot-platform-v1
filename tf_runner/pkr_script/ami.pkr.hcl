packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  subnet_id = "subnet-c59e05ad"
  security_group_id = "sg-05be52eaee4eae863"
  ssh_username  = "ubuntu"
  instance_type = "t2.micro"
  region        = "us-east-2"
  source_ami    = "ami-0fb653ca2d3203ac1"
  ami_name      = "learn-packer-linux-aws"
}

build {
  name = "packer"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]
}
