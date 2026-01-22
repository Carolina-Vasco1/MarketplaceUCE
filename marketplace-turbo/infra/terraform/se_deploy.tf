resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "deploy" {
  bucket        = "${var.project_name}-deploy-${random_id.suffix.hex}"
  force_destroy = true
}

resource "aws_s3_object" "compose" {
  bucket       = aws_s3_bucket.deploy.id
  key          = "docker-compose.aws.yml"
  source       = "${path.module}/docker-compose.aws.yml"
  content_type = "text/yaml"
  etag         = filemd5("${path.module}/docker-compose.aws.yml")
}
