variable "region" {
  type    = string
  default = "us-east-1"
}

variable "app_name" {
  type    = string
  default = "marketplaceuce"
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}

# Debe existir en tu cuenta AWS Academy (EC2 -> Key pairs)
variable "key_name" {
  type = string
}

# Tu IP pública para SSH al bastion (ej: "181.12.34.56/32")
variable "my_ip_cidr" {
  type = string
}

# Si ya tienes una AMI propia, ponla aquí (recomendado)
# Si lo dejas vacío, usará Amazon Linux 2023
variable "app_ami_id" {
  type    = string
  default = ""
}

# Puerto del gateway dentro de EC2 (tu gateway corre en 8000)
variable "app_port" {
  type    = number
  default = 8000
}
