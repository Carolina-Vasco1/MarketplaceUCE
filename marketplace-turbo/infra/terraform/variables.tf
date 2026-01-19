variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "marketplaceuce"
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

# Para que el front (Vercel o tu dominio) pueda consumir el API
variable "frontend_origin" {
  type    = string
  default = "http://localhost:5173"
}

# CPU/Mem por servicio
variable "task_cpu" {
  type    = number
  default = 256
}

variable "task_memory" {
  type    = number
  default = 512
}

# Puerto expuesto por el gateway internamente
variable "gateway_container_port" {
  type    = number
  default = 8000
}

# puertos internos de servicios (solo ECS)
variable "auth_port"          { type = number default = 8001 }
variable "product_port"       { type = number default = 8002 }
variable "order_port"         { type = number default = 8003 }
variable "payment_port"       { type = number default = 8004 }
variable "notification_port"  { type = number default = 8005 }
variable "blockchain_port"    { type = number default = 8006 }

# Variables sensibles (puedes dejarlas vacías y luego setear en ECS)
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

variable "paypal_client_secret" {
  type      = string
  sensitive = true
  default   = ""
}

variable "paypal_env" {
  type    = string
  default = "sandbox"
}
