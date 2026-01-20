locals {
  name = "${var.project_name}-${var.env}"
  tags = {
    Project = var.project_name
    Env     = var.env
  }
}

resource "aws_ecs_cluster" "cluster" {
  name = "${var.project_name}-cluster"
  tags = local.tags
}