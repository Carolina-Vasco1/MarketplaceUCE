resource "aws_security_group" "app_sg" {
  name        = "${var.project_name}-app-sg"
  description = "EC2 app security group"
  vpc_id      = aws_vpc.main.id

  # SSH SOLO desde Bastion
  ingress {
    description     = "SSH from Bastion only"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = var.enable_bastion ? [aws_security_group.bastion_sg[0].id] : []
  }

  # Gateway SOLO desde el ALB (puerto 8000)
  ingress {
    description     = "Gateway from ALB"
    from_port       = var.gateway_container_port
    to_port         = var.gateway_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, { Name = "${var.project_name}-app-sg" })
}
