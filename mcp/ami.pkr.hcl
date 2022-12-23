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
  ami_name      = "mcp-${var.ami_name}"
  source_ami    = "ami-09e67e426f25ce0d7"

  tags = {
    Provisioner = "Packer"
    Name        = "mcp-${var.ami_name}"
  }
}


build {
  name    = "packer"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]

  provisioner "file" {
    source      = "./../mcp"
    destination = "/home/ubuntu"
  }

  provisioner "shell" {
    script = "remote_services.sh"
    environment_vars = [
        "DEBIAN_FRONTEND=noninteractive"
    ]
  }

  provisioner "shell" {
    inline = [
        "rm -rf /home/ubuntu/mcp/remote_services.sh"
    ]
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }

  post-processor "shell-local" {
    inline = [
      "bash local-exec-script.sh"
    ]
  }
}

Alvira Khan
Reshma Khan
Zaffar Khan