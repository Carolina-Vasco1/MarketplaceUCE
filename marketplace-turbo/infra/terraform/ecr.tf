locals {
  services = [
    "gateway",
    "auth-service",
    "product-service",
    "order-service",
    "payment-service",
    "notification-service",
    "blockchain-service",
    "frontend"
  ]
}

resource "aws_ecr_repository" "repos" {
  for_each = toset(local.services)
  name     = "${var.project_name}/${each.value}"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "${var.project_name}-${each.value}" }
}

output "ecr_repo_urls" {
  value = { for k, v in aws_ecr_repository.repos : k => v.repository_url }
}
