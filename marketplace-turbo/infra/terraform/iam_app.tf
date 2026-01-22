data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "ec2_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "app_role" {
  name               = "${var.project_name}-app-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json
}

# Leer imágenes de ECR
resource "aws_iam_role_policy_attachment" "ecr_readonly" {
  role      = aws_iam_role.app_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# Leer el compose desde S3
data "aws_iam_policy_document" "s3_get_compose" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.deploy.arn}/${aws_s3_object.compose.key}"]
  }
}

resource "aws_iam_policy" "s3_get_compose" {
  name   = "${var.project_name}-s3-get-compose"
  policy = data.aws_iam_policy_document.s3_get_compose.json
}

resource "aws_iam_role_policy_attachment" "s3_get_compose_attach" {
  role      = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.s3_get_compose.arn
}

resource "aws_iam_instance_profile" "app_profile" {
  name = "${var.project_name}-app-profile"
  role = aws_iam_role.app_role.name
}

data "aws_iam_policy_document" "ssm_read" {
  statement {
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:GetParametersByPath"
    ]
    resources = [
      "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/${var.project_name}/qa/*",
      "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/${var.project_name}/qa/*"
    ]
  }
}

resource "aws_iam_policy" "ssm_read" {
  name   = "${var.project_name}-ssm-read"
  policy = data.aws_iam_policy_document.ssm_read.json
}

resource "aws_iam_role_policy_attachment" "ssm_read_attach" {
  role      = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.ssm_read.arn
}
