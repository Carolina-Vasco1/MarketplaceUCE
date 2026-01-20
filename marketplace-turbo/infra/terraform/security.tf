resource "aws_security_group" "alb_sg" {
  name        = "${var.project_name}-alb-sg"
  description = "ALB security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from Internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, { Name = "${var.project_name}-alb-sg" })
}

resource "aws_security_group" "ecs_tasks_sg" {
  name        = "${var.project_name}-ecs-tasks-sg"
  description = "ECS tasks security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Gateway from ALB"
    from_port       = var.gateway_container_port
    to_port         = var.gateway_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  # ✅ Admin/debug SOLO desde Bastion (opcional)
  dynamic "ingress" {
    for_each = var.enable_bastion ? [1] : []
    content {
      description     = "Admin from Bastion"
      from_port       = 0
      to_port         = 65535
      protocol        = "tcp"
      security_groups = [aws_security_group.bastion_sg[0].id]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, { Name = "${var.project_name}-ecs-tasks-sg" })
}
