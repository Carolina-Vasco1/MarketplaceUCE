output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "gateway_url" {
  value = "http://${aws_lb.alb.dns_name}"
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "bastion_public_ip" {
  value = var.enable_bastion ? aws_instance.bastion[0].public_ip : null
}

output "bastion_ssh" {
  value = var.enable_bastion ? "ssh -i <TU_PEM>.pem ec2-user@${aws_instance.bastion[0].public_ip}" : null
}
