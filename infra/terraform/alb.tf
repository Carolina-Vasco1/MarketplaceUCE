resource "aws_lb" "alb" {
  name               = "${var.app_name}-alb"
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_a.id]
}

resource "aws_lb_target_group" "tg" {
  name     = "${var.app_name}-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = aws_vpc.this.id
  health_check {
    path = "/docs"
    port = "8000"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}
