output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "gateway_url" {
  value = "http://${aws_instance.app.public_dns}:${var.gateway_container_port}"

}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "ecs_cluster_name" {
  value = data.aws_ecs_cluster.cluster.cluster_name
}

