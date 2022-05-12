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
