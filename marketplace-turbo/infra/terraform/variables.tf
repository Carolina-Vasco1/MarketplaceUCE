variable "project_name" {
  type    = string
  default = "marketplaceuce-qa"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "public_subnets" {
  type    = list(string)
  default = ["10.20.1.0/24", "10.20.2.0/24"]
}

variable "private_subnets" {
  type    = list(string)
  default = ["10.20.11.0/24", "10.20.12.0/24"]
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "key_name" {
  type        = string
  description = "KeyPair existente en AWS"
}

variable "allowed_ssh_cidr" {
  type        = string
  description = "IP publica para SSH al bastion (x.x.x.x/32)"
}

variable "app_port" {
  type    = number
  default = 8000
}

variable "app_image" {
  type    = string
  default = "nginx:alpine"
}

variable "app_container_name" {
  type    = string
  default = "app"
}

variable "enable_nat" {
  type    = bool
  default = false
}

variable "asg_min" {
  type    = number
  default = 1
}

variable "asg_max" {
  type    = number
  default = 2
}

variable "asg_desired" {
  type    = number
  default = 1
}

# 🔽 PUERTOS (si los necesitas más adelante)
variable "auth_port" {
  type    = number
  default = 8001
}

variable "product_port" {
  type    = number
  default = 8002
}

variable "order_port" {
  type    = number
  default = 8003
}

variable "payment_port" {
  type    = number
  default = 8004
}

variable "notification_port" {
  type    = number
  default = 8005
}

variable "blockchain_port" {
  type    = number
  default = 8006
}
