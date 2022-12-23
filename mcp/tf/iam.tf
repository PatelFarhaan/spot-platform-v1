// S3 Bucket Policy
resource "aws_iam_policy" "s3_bucket_policy" {
  description = "Full S3 bucket permission"
  name        = "mcp-s3-${var.aws_region}-${var.env}"
  path        = "/mcp/${var.env}/${var.aws_region}/"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Effect   = "Allow",
        Action   = "s3:*",
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.artifactory_s3_bucket.id}/*",
          "arn:aws:s3:::${aws_s3_bucket.artifactory_s3_bucket.id}",
        ]
      }
    ]
  })
}


// Creating a IAM Role
resource "aws_iam_role" "permission_for_artifactory" {
  name                = "mcp-${var.aws_region}-${var.env}"
  managed_policy_arns = [
    aws_iam_policy.s3_bucket_policy.arn
  ]

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Effect    = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        },
        Action    = "sts:AssumeRole"
      }
    ]
  })

  tags =var.tags
}
