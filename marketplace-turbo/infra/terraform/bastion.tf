# =========================
# Bastion Host (Admin only)
# =========================

variable "enable_bastion" {
  type    = bool
  default = true
}

variable "my_ip_cidr" {
  type        = string
  description = "Tu IP pública en /32 (ej: 190.xxx.xxx.xxx/32) para permitir SSH al bastion"
  default     = "0.0.0.0/0"
}

variable "bastion_instance_type" {
  type    = string
  default = "t3.micro"
}

data "aws_ami" "al2023_bastion" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_security_group" "bastion_sg" {
  count       = var.enable_bastion ? 1 : 0
  name        = "${var.project_name}-bastion-sg"
  description = "Bastion SG (SSH only from my IP)"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, { Name = "${var.project_name}-bastion-sg" })
}

resource "aws_instance" "bastion" {
  count                  = var.enable_bastion ? 1 : 0
  ami                    = data.aws_ami.al2023_bastion.id
  instance_type          = var.bastion_instance_type
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.bastion_sg[0].id]
  key_name               = var.key_name != "" ? var.key_name : null

  tags = merge(local.tags, { Name = "${local.name}-bastion" })
}

output "bastion_public_ip" {
  value = var.enable_bastion ? aws_instance.bastion[0].public_ip : null
}

output "bastion_ssh" {
  value = var.enable_bastion ? "ssh -i <TU_PEM>.pem ec2-user@${aws_instance.bastion[0].public_ip}" : null
}
