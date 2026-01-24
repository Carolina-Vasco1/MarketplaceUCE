output "alb_dns_name" {
  value       = aws_lb.alb.dns_name
  description = "Application Load Balancer DNS name"
}

output "alb_url" {
  value       = "http://${aws_lb.alb.dns_name}"
  description = "Application Load Balancer URL"
}

output "bastion_public_ip" {
  value       = aws_instance.bastion.public_ip
  description = "Bastion public IP"
}

output "ssh_bastion" {
  value       = "ssh -i <TU_PEM>.pem ec2-user@${aws_instance.bastion.public_ip}"
  description = "SSH command to bastion"
}

output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
}

output "ecr_registry" {
  value       = replace(aws_ecr_repository.images["marketplace-gateway"].repository_url, "/marketplace-gateway", "")
  description = "ECR Registry URL"
}

output "ecr_repositories" {
  value = {
    for name, repo in aws_ecr_repository.images :
    name => repo.repository_url
  }
  description = "All ECR repository URLs"
}

output "ecr_login_command" {
  value       = "aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.${var.region}.amazonaws.com"
  description = "Command to login to ECR"
}

output "docker_compose_push_command" {
  value       = "bash ${path.module}/push-to-ecr.sh ${var.region} ${var.image_tag}"
  description = "Command to push Docker Hub images to ECR"
}
