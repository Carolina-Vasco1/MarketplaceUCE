data "aws_ami" "al2023" {
  count       = var.app_ami_id == "" ? 1 : 0
  most_recent = true
  owners      = ["amazon"]

  data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64*"]
  }
}

locals {
  chosen_ami = var.app_ami_id != "" ? var.app_ami_id : data.aws_ami.al2023[0].id
}

resource "aws_launch_template" "lt" {
  name_prefix   = "${var.app_name}-lt-"
  image_id      = local.chosen_ami
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  user_data = base64encode(file("${path.module}/user_data.sh"))

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.app_name}-app"
    }
  }
}

resource "aws_autoscaling_group" "asg" {
  name             = "${var.app_name}-asg"
  desired_capacity = 1
  max_size         = 2
  min_size         = 1

  vpc_zone_identifier = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]

  launch_template {
    id      = aws_launch_template.lt.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.tg.arn]

  health_check_type         = "ELB"
  health_check_grace_period = 120

  tag {
    key                 = "Name"
    value               = "${var.app_name}-asg-instance"
    propagate_at_launch = true
  }
}
