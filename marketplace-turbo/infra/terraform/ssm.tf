resource "aws_ssm_parameter" "jwt_secret" {
  name  = "/${var.project_name}/qa/JWT_SECRET"
  type  = "SecureString"
  value = var.jwt_secret
}

resource "aws_ssm_parameter" "frontend_origin" {
  name  = "/${var.project_name}/qa/FRONTEND_ORIGIN"
  type  = "String"
  value = var.frontend_origin
}

resource "aws_ssm_parameter" "paypal_base_url" {
  name  = "/${var.project_name}/qa/PAYPAL_BASE_URL"
  type  = "String"
  value = var.paypal_base_url
}

resource "aws_ssm_parameter" "paypal_client_id" {
  name  = "/${var.project_name}/qa/PAYPAL_CLIENT_ID"
  type  = "SecureString"
  value = var.paypal_client_id
}

resource "aws_ssm_parameter" "paypal_client_secret" {
  name  = "/${var.project_name}/qa/PAYPAL_CLIENT_SECRET"
  type  = "SecureString"
  value = var.paypal_client_secret
}

resource "aws_ssm_parameter" "paypal_webhook_id" {
  name  = "/${var.project_name}/qa/PAYPAL_WEBHOOK_ID"
  type  = "String"
  value = var.paypal_webhook_id
}

resource "aws_ssm_parameter" "paypal_env" {
  name  = "/${var.project_name}/qa/PAYPAL_ENV"
  type  = "String"
  value = var.paypal_env
}

resource "aws_ssm_parameter" "smtp_host" {
  name  = "/${var.project_name}/qa/SMTP_HOST"
  type  = "String"
  value = var.smtp_host
}

resource "aws_ssm_parameter" "smtp_port" {
  name  = "/${var.project_name}/qa/SMTP_PORT"
  type  = "String"
  value = var.smtp_port
}

resource "aws_ssm_parameter" "smtp_user" {
  name  = "/${var.project_name}/qa/SMTP_USER"
  type  = "SecureString"
  value = var.smtp_user
}

resource "aws_ssm_parameter" "smtp_password" {
  name  = "/${var.project_name}/qa/SMTP_PASSWORD"
  type  = "SecureString"
  value = var.smtp_password
}

resource "aws_ssm_parameter" "smtp_from" {
  name  = "/${var.project_name}/qa/SMTP_FROM"
  type  = "String"
  value = var.smtp_from
}

resource "aws_ssm_parameter" "mongo_url" {
  name  = "/${var.project_name}/qa/MONGO_URL"
  type  = "String"
  value = var.mongo_url
}

resource "aws_ssm_parameter" "mongo_db" {
  name  = "/${var.project_name}/qa/MONGO_DB"
  type  = "String"
  value = var.mongo_db
}

variable "jwt_secret" { type = string; sensitive = true }
variable "frontend_origin" { type = string }

variable "paypal_base_url" { type = string }
variable "paypal_client_id" { type = string; sensitive = true }
variable "paypal_client_secret" { type = string; sensitive = true }
variable "paypal_webhook_id" { type = string }
variable "paypal_env" { type = string }

variable "smtp_host" { type = string }
variable "smtp_port" { type = string }
variable "smtp_user" { type = string; sensitive = true }
variable "smtp_password" { type = string; sensitive = true }
variable "smtp_from" { type = string }

variable "mongo_url" { type = string }
variable "mongo_db" { type = string }
