output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "gateway_url" {
  value = "http://${aws_lb.alb.dns_name}"
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "ecs_cluster" {
  value = aws_ecs_cluster.cluster.name
}
