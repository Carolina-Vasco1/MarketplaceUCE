############################
# Core
############################
variable "project_name" {
  type        = string
  description = "Nombre base del proyecto/stack"
  default     = "marketplaceuce-qa"
}

variable "region" {
  type        = string
  description = "Región AWS"
  default     = "us-east-1"
}

############################
# Networking
############################
variable "vpc_cidr" {
  type        = string
  description = "CIDR del VPC"
  default     = "10.20.0.0/16"
}

variable "public_subnets" {
  type        = list(string)
  description = "CIDRs de subnets públicas"
  default     = ["10.20.1.0/24", "10.20.2.0/24"]
}

variable "private_subnets" {
  type        = list(string)
  description = "CIDRs de subnets privadas"
  default     = ["10.20.11.0/24", "10.20.12.0/24"]
}

variable "enable_nat" {
  type        = bool
  description = "Habilitar NAT Gateway para subnets privadas"
  default     = false
}

############################
# Compute / Access
############################
variable "instance_type" {
  type        = string
  description = "Tipo de instancia EC2"
  default     = "t3.micro"
}

variable "ami_id" {
  type        = string
  description = "AMI ID personalizada (deja vacío para usar el default Amazon Linux 2023)"
  default     = ""
}

variable "key_name" {
  type        = string
  description = "KeyPair existente en AWS (para SSH)"
}

variable "key_name_path" {
  type        = string
  description = "Ruta al archivo .pem de la key privada"
  default     = ""
}

variable "allowed_ssh_cidr" {
  type        = string
  description = "IP pública permitida para SSH al bastion (x.x.x.x/32)"
}

############################
# App / Ports / ASG
############################
variable "app_port" {
  type        = number
  description = "Puerto expuesto por el gateway detrás del ALB"
  default     = 8000
}

variable "asg_min" {
  type        = number
  description = "Mínimo de instancias en el Auto Scaling Group"
  default     = 1
}

variable "asg_max" {
  type        = number
  description = "Máximo de instancias en el Auto Scaling Group"
  default     = 2
}

variable "asg_desired" {
  type        = number
  description = "Deseado de instancias en el Auto Scaling Group"
  default     = 1
}

############################
# Docker images
############################
variable "dockerhub_user" {
  type        = string
  description = "Docker Hub username/org que hostea las imágenes"
}

variable "image_tag" {
  type        = string
  description = "Tag de las imágenes"
  default     = "qa"
}