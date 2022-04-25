#resource "aws_ebs_volume" "example" {
#  availability_zone = "us-west-2a"
#  size              = 40
#
#  tags = {
#    Name = "HelloWorld"
#  }
#}
#
#resource "aws_ebs_snapshot" "example_snapshot" {
#  volume_id = aws_ebs_volume.example.id
#
#  tags = {
#    Name = "HelloWorld_snap"
#  }
#}
##https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot