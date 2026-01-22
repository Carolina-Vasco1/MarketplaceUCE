#!/bin/bash
set -e

# Log para depurar
exec > >(tee /var/log/userdata.log | logger -t userdata -s 2>/dev/console) 2>&1

dnf update -y
dnf install -y docker awscli

systemctl enable docker
systemctl start docker

# Docker Compose plugin (Amazon Linux 2023)
mkdir -p /usr/local/lib/docker/cli-plugins
curl -sSL https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Login a ECR (si usas ECR)
aws ecr get-login-password --region ${AWS_REGION} | docker login \
  --username AWS --password-stdin ${ECR_REGISTRY}

mkdir -p /opt/marketplace
cd /opt/marketplace

# Descargar docker-compose desde S3
aws s3 cp s3://${DEPLOY_BUCKET}/docker-compose.aws.yml docker-compose.yml

# Construye .env desde SSM
PARAM_BASE="/${PROJECT_NAME}/qa"

getp () {
  aws ssm get-parameter --with-decryption --name "$1" --region ${AWS_REGION} --query "Parameter.Value" --output text
}

cat > .env <<EOF
JWT_SECRET=$(getp ${PARAM_BASE}/JWT_SECRET)
FRONTEND_ORIGIN=$(getp ${PARAM_BASE}/FRONTEND_ORIGIN)

PAYPAL_BASE_URL=$(getp ${PARAM_BASE}/PAYPAL_BASE_URL)
PAYPAL_CLIENT_ID=$(getp ${PARAM_BASE}/PAYPAL_CLIENT_ID)
PAYPAL_CLIENT_SECRET=$(getp ${PARAM_BASE}/PAYPAL_CLIENT_SECRET)
PAYPAL_WEBHOOK_ID=$(getp ${PARAM_BASE}/PAYPAL_WEBHOOK_ID)
PAYPAL_ENV=$(getp ${PARAM_BASE}/PAYPAL_ENV)

SMTP_HOST=$(getp ${PARAM_BASE}/SMTP_HOST)
SMTP_PORT=$(getp ${PARAM_BASE}/SMTP_PORT)
SMTP_USER=$(getp ${PARAM_BASE}/SMTP_USER)
SMTP_PASSWORD=$(getp ${PARAM_BASE}/SMTP_PASSWORD)
SMTP_FROM=$(getp ${PARAM_BASE}/SMTP_FROM)

MONGO_URL=$(getp ${PARAM_BASE}/MONGO_URL)
MONGO_DB=$(getp ${PARAM_BASE}/MONGO_DB)
EOF


# Levantar todo
docker compose --env-file .env up -d

docker ps
