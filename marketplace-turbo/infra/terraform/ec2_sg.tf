resource "aws_security_group" "app_sg" {
  name        = "${var.project_name}-app-sg"
  description = "EC2 app security group"
  vpc_id      = aws_vpc.main.id

  # SSH SOLO desde el Bastion
  ingress {
    description     = "SSH from Bastion only"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = var.enable_bastion ? [aws_security_group.bastion_sg[0].id] : []
  }

  # HTTP solo si necesitas entrar directo a la EC2 (yo recomendaría NO)
  ingress {
    description = "HTTP"
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

  tags = merge(local.tags, { Name = "${var.project_name}-app-sg" })
}
