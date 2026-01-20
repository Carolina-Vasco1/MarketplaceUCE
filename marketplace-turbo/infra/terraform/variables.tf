variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "marketplaceuce"
}

variable "env" {
  type    = string
  default = "lab"
}

# Networking
variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "public_subnets" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  type    = list(string)
  default = ["10.0.11.0/24", "10.0.12.0/24"]
}

# EC2
variable "instance_type" {
  type    = string
  default = "t3.medium"
}

variable "key_name" {
  type    = string
  default = "" # pon tu KeyPair si usaras SSH
}

# Proyecto (repo)
variable "git_repo_url" {
  type    = string
  default = "" # ejemplo: https://github.com/tuUsuario/marketplaceUCE.git
}

variable "git_branch" {
  type    = string
  default = "main"
}

variable "gateway_container_port" {
  type    = number
  default = 8000
}

variable "frontend_port" {
  type    = number
  default = 80
}

# =========================
# Bastion
# =========================

variable "enable_bastion" {
  type    = bool
  default = true
}


variable "bastion_instance_type" {
  type    = string
  default = "t3.micro"
}

variable "my_ip_cidr" {
  type        = string
  description = "Tu IP publica en /32 para permitir SSH al bastion (ej: 190.x.x.x/32)"
  default     = "0.0.0.0/0"
}

variable "frontend_origin" {
  type    = string
  default = "http://localhost:5173"
}

variable "paypal_client_secret" {
  type      = string
  sensitive = true
  default   = ""
}

variable "jwt_secret" {
  type      = string
  sensitive = true
  default   = "dev_secret_change_me"
}

variable "paypal_client_id" {
  type      = string
  sensitive = true
  default   = ""
}

variable "paypal_env" {
  type    = string
  default = "sandbox"
}
