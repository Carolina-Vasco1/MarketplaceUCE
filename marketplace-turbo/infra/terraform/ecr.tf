###########################
# ECR Repositories
###########################
locals {
  ecr_images = [
    "marketplace-gateway",
    "marketplace-auth",
    "marketplace-product",
    "marketplace-order",
    "marketplace-payment",
    "marketplace-notification",
    "marketplace-blockchain",
    "marketplace-category",
    "marketplace-ai",
    "marketplace-admin",
    "marketplace-search",
    "marketplace-user",
    "marketplace-review",
    "marketplace-ad-connector",
    "marketplace-reporting",
  ]
}

resource "aws_ecr_repository" "images" {
  for_each = toset(local.ecr_images)

  name                 = each.value
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name = "${local.name}-${each.value}"
  }
}

resource "aws_ecr_lifecycle_policy" "cleanup" {
  for_each = aws_ecr_repository.images

  repository = each.value.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
