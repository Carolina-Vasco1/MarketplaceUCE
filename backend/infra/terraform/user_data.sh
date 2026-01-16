#!/bin/bash
set -e

dnf update -y
dnf install -y docker git
systemctl enable docker
systemctl start docker

# docker compose plugin
dnf install -y docker-compose-plugin

cd /opt
rm -rf MarketplaceUCE || true

# ✅ Tu repo real + branch QA
git clone -b qa https://github.com/Carolina-Vasco1/MarketplaceUCE.git
cd MarketplaceUCE

# ✅ Generar .env para backend (AJUSTA ESTOS VALORES)
cat > .env <<'EOF'
JWT_SECRET=CAMBIA_ESTE_JWT_SECRET_ULTRA_LARGO_Y_SEGURO
FRONTEND_ORIGIN=https://TU-FRONTEND.vercel.app

PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com
PAYPAL_CLIENT_ID=TU_PAYPAL_SANDBOX_CLIENT_ID_REAL
PAYPAL_CLIENT_SECRET=TU_PAYPAL_SANDBOX_CLIENT_SECRET_REAL
PAYPAL_WEBHOOK_ID=

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=jasanchezc3@gmail.com
SMTP_PASSWORD=APP_PASSWORD_NUEVA_DE_GMAIL
SMTP_FROM=Marketplace UCE <jasanchezc3@gmail.com>
EOF

docker compose up -d --build

docker ps -a > /opt/containers_status.txt
docker compose logs --tail=200 > /opt/compose_logs_tail.txt
