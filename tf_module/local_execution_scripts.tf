resource "null_resource" "infracost_estimation" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command     = <<-EOT
      infracost breakdown --path ${path.root} --terraform-parse-hcl --format json --out-file infracost-base.json
      infracost output --path infracost-base.json --format table --show-skipped
    EOT
  }
}


resource "null_resource" "update_elb_in_s3" {
  depends_on = [aws_alb.load_balancer]

  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command     = <<-EOT
      bucket_name=spot-platform
      object_name=alb_links.json

      cd /tmp
      rm -f $object_name

      object_exists=$(aws s3api head-object --bucket $bucket_name --key docker-agents/$object_name || true)
      if [ -z "$object_exists" ]; then
        echo "$object_name does not exist. New one will be created"
        echo $(echo '{"${aws_alb.load_balancer.dns_name}": "${var.app_name}-${var.env}"}' | jq .) > $object_name
        aws s3 cp ./$object_name s3://$bucket_name/docker-agents/
      else
        echo "$object_name exists!!!"
        aws s3 cp s3://$bucket_name/docker-agents/$object_name ./
        dns_exists=$(cat $object_name | jq 'has("${aws_alb.load_balancer.dns_name}")')
        echo "ALB exists: $dns_exists"

        if [ $dns_exists == true ];
        then
          echo "Alb link is present!!!"
        else
          echo "Adding Alb dns..."
          cat $object_name
          echo $(jq '."${aws_alb.load_balancer.dns_name}"="${var.app_name}-${var.env}"' $object_name) > $object_name
          aws s3 cp ./$object_name s3://$bucket_name/docker-agents/
        fi
      fi
    EOT
  }
}


resource "null_resource" "delete_elb_in_s3" {
  triggers = {
    alb_dns = aws_alb.load_balancer.dns_name
  }

  provisioner "local-exec" {
    when = destroy
    command     = <<-EOT
      set -e -x

      bucket_name=spot-platform
      object_name=alb_links.json

      cd /tmp
      rm -f $object_name

      aws s3 cp s3://$bucket_name/docker-agents/$object_name ./
      echo $(jq 'del(."${self.triggers.alb_dns}")' $object_name) > $object_name
      aws s3 cp ./$object_name s3://$bucket_name/docker-agents/

    EOT
  }
}
