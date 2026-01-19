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
  default = "dev"
}

# Tus imágenes en ECR (tag latest por defecto)
variable "images" {
  type = map(string)
  default = {
    gateway            = "gateway:latest"
    auth_service       = "auth-service:latest"
    product_service    = "product-service:latest"
    order_service      = "order-service:latest"
    payment_service    = "payment-service:latest"
    notification_service = "notification-service:latest"
    blockchain_service = "blockchain-service:latest"
    frontend           = "frontend:latest"
  }
}

# Puertos internos (contenedor)
variable "ports" {
  type = map(number)
  default = {
    gateway              = 8000
    auth_service         = 8001
    product_service      = 8002
    order_service        = 8003
    payment_service      = 8004
    notification_service = 8005
    blockchain_service   = 8006
    frontend             = 80
  }
}

# ==== Config de entorno (NO metas secretos aquí si puedes evitarlo) ====
variable "jwt_secret" {
  type      = string
  sensitive = true
}

variable "frontend_origin" {
  type    = string
  default = "http://localhost"
}

# URLs internas (en ECS se resuelven por DNS del service discovery o ALB interno)
# aquí las dejamos como variables para que puedas cambiarlas.
variable "paypal_client_id" {
  type      = string
  sensitive = true
  default   = ""
}
variable "paypal_env" {
  type    = string
  default = "sandbox"
}

# Infra URLs (si lo corres fuera o dentro)
variable "mongo_url" {
  type    = string
  default = ""
}
variable "mongo_db" {
  type    = string
  default = "marketUce"
}
variable "redis_url" {
  type    = string
  default = ""
}
variable "kafka_bootstrap" {
  type    = string
  default = ""
}
