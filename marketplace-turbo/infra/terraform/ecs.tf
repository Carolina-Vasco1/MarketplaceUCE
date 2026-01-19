resource "aws_ecs_cluster" "cluster" {
  name = "${var.project_name}-cluster"
}

resource "aws_cloudwatch_log_group" "logs" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 7
}

# Subredes privadas para ECS
locals {
  private_subnet_ids = [for s in aws_subnet.private : s.id]
}

# --------- Task Definition (Gateway)
resource "aws_ecs_task_definition" "gateway" {
  family                   = "${var.project_name}-gateway"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "gateway"
      image     = "${aws_ecr_repository.repos["gateway"].repository_url}:latest"
      essential = true
      portMappings = [
        { containerPort = var.gateway_container_port, hostPort = var.gateway_container_port, protocol = "tcp" }
      ]
      environment = [
        { name = "JWT_SECRET", value = var.jwt_secret },
        { name = "JWT_ALG", value = "HS256" },
        { name = "FRONTEND_ORIGIN", value = var.frontend_origin },

        { name = "AUTH_URL", value = "http://auth-service:8001" },
        { name = "PRODUCT_URL", value = "http://product-service:8002" },
        { name = "ORDER_URL", value = "http://order-service:8003" },
        { name = "PAYMENT_URL", value = "http://payment-service:8004" },
        { name = "NOTIF_URL", value = "http://notification-service:8005" },
        { name = "BLOCKCHAIN_URL", value = "http://blockchain-service:8006" },

        { name = "PAYPAL_ENV", value = var.paypal_env },
        { name = "PAYPAL_CLIENT_ID", value = var.paypal_client_id }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "gateway"
        }
      }
    }
  ])
}

# --------- Generic microservice task definition builder (sin ALB)
locals {
  microservices = {
    "auth-service" = var.auth_port
    "product-service" = var.product_port
    "order-service" = var.order_port
    "payment-service" = var.payment_port
    "notification-service" = var.notification_port
    "blockchain-service" = var.blockchain_port
  }
}

resource "aws_ecs_task_definition" "micro" {
  for_each                 = local.microservices
  family                   = "${var.project_name}-${each.key}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = each.key
      image     = "${aws_ecr_repository.repos[each.key].repository_url}:latest"
      essential = true
      portMappings = [
        { containerPort = each.value, hostPort = each.value, protocol = "tcp" }
      ]
      environment = [
        { name = "JWT_SECRET", value = var.jwt_secret },
        { name = "JWT_ALG", value = "HS256" },

        # PayPal solo para payment-service
        { name = "PAYPAL_ENV", value = var.paypal_env },
        { name = "PAYPAL_CLIENT_ID", value = var.paypal_client_id },
        { name = "PAYPAL_CLIENT_SECRET", value = var.paypal_client_secret },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = each.key
        }
      }
    }
  ])
}

# --------- ECS Services
resource "aws_ecs_service" "gateway" {
  name            = "${var.project_name}-gateway"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.gateway.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = local.private_subnet_ids
    security_groups = [aws_security_group.ecs_tasks_sg.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.gateway_tg.arn
    container_name   = "gateway"
    container_port   = var.gateway_container_port
  }

  depends_on = [aws_lb_listener.http]
}

resource "aws_ecs_service" "micro" {
  for_each        = local.microservices
  name            = "${var.project_name}-${each.key}"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.micro[each.key].arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = local.private_subnet_ids
    security_groups = [aws_security_group.ecs_tasks_sg.id]
    assign_public_ip = false
  }
}
