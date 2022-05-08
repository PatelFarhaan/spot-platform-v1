packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}


variable "ami_name" {
  type = string
}


source "amazon-ebs" "ubuntu" {
  ssh_username  = "ubuntu"
  instance_type = "t2.medium"
  region        = "us-east-1"
  ami_name      = var.ami_name
  source_ami    = "ami-09e67e426f25ce0d7"

  tags = {
    Provisioner = "Packer"
    Name        = var.ami_name
  }
}


build {
  name    = "packer"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]

  provisioner "file" {
    source      = "./../ami"
    destination = "/tmp"
  }

  provisioner "shell" {
    inline = [
      "sudo mkdir -p /var/opt/spotops/agents",
      "sudo mv /tmp/ami/spotops_script.sh /var/opt/spotops/agents/"
    ]
    environment_vars = [
        "DEBIAN_FRONTEND=noninteractive"
    ]
  }

  provisioner "shell" {
    script = "spotops_script.sh"
    environment_vars = [
        "DEBIAN_FRONTEND=noninteractive"
    ]
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
