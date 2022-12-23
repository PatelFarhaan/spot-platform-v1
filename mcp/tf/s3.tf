// Creating a log bucket
resource "aws_s3_bucket" "artifactory_log_bucket" {
  force_destroy = true
  acl           = "log-delivery-write"
  bucket        = var.s3_log_bucket_name
}


// Creating an S3 bucket
resource "aws_s3_bucket" "artifactory_s3_bucket" {
  force_destroy = true
  acl           = "private"
  bucket_prefix = var.s3_artifactory_bucket_name

  versioning {
    enabled = true
  }

  logging {
    target_prefix = "log/"
    target_bucket = aws_s3_bucket.artifactory_log_bucket.id
  }

  tags = merge(var.tags, {
    "stack" = "mcp-${var.aws_region}-${var.env}",
    "Name"  = "mcp-${var.aws_region}-${var.env}"
  })
}
