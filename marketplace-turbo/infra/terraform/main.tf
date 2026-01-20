locals {
  name = "${var.project_name}-${var.env}"
  tags = {
    Project = var.project_name
    Env     = var.env
  }
}
data "aws_ecs_cluster" "cluster" {
  cluster_name = "${var.project_name}-cluster"
}
