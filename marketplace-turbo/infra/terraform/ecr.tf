resource "aws_ecr_repository" "repos" {
  for_each = toset([
    "frontend",
    "gateway",
    "auth-service",
    "product-service",
    "order-service",
    "payment-service",
    "notification-service",
    "blockchain-service"
  ])

  name                 = "${var.project_name}/${each.key}"
  image_tag_mutability = "MUTABLE"
}
