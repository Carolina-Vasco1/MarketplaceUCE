resource "aws_lb_target_group" "gateway_tg" {
  name        = "${var.project_name}-gw-tg"
  port        = var.gateway_container_port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"

  health_check {
    enabled             = true
    path                = "/health"
    matcher             = "200-399"
    interval            = 20
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group_attachment" "app_gateway" {
  target_group_arn = aws_lb_target_group.gateway_tg.arn
  target_id        = aws_instance.app.id
  port             = var.gateway_container_port
}
