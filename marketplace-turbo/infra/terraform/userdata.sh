#!/bin/bash
set -e
exec > >(tee /var/log/userdata.log | logger -t userdata -s 2>/dev/console) 2>&1

dnf update -y
dnf install -y docker curl

systemctl enable docker
systemctl start docker

# Docker Compose plugin (Amazon Linux 2023)
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

mkdir -p /opt/marketplace
cd /opt/marketplace

cat > docker-compose.yml <<YAML
services:
  gateway:
    image: ${DOCKERHUB_USER}/marketplace-gateway:${TAG}
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      JWT_SECRET: "dev_secret_change_me"
      JWT_ALG: "HS256"
      FRONTEND_ORIGIN: "*"
      AUTH_URL: http://auth-service:8001
      PRODUCT_URL: http://product-service:8002
      ORDER_URL: http://order-service:8003
      PAYMENT_URL: http://payment-service:8004
      NOTIF_URL: http://notification-service:8005
      BLOCKCHAIN_URL: http://blockchain-service:8006
    depends_on:
      - auth-service
      - product-service
      - order-service
      - payment-service
      - notification-service
      - blockchain-service

  auth-service:
    image: ${DOCKERHUB_USER}/marketplace-auth:${TAG}
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      POSTGRES_URL: postgresql+asyncpg://auth:auth@postgres:5432/auth_db
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET: "dev_secret_change_me"
      JWT_ALG: "HS256"
    depends_on:
      - postgres
      - redis

  product-service:
    image: ${DOCKERHUB_USER}/marketplace-product:${TAG}
    restart: unless-stopped
    ports:
      - "8002:8002"
    environment:
      MONGO_URL: mongodb://mongo:27017
      MONGO_DB: marketUce
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET: "dev_secret_change_me"
      JWT_ALG: "HS256"
    depends_on:
      - mongo
      - redis

  order-service:
    image: ${DOCKERHUB_USER}/marketplace-order:${TAG}
    restart: unless-stopped
    ports:
      - "8003:8003"
    environment:
      POSTGRES_URL: postgresql+asyncpg://order:order@postgres:5432/order_db
      KAFKA_BOOTSTRAP: kafka:29092
      JWT_SECRET: "dev_secret_change_me"
      JWT_ALG: "HS256"
    depends_on:
      - postgres
      - kafka

  payment-service:
    image: ${DOCKERHUB_USER}/marketplace-payment:${TAG}
    restart: unless-stopped
    ports:
      - "8004:8004"
    environment:
      KAFKA_BOOTSTRAP: kafka:29092
      PAYPAL_ENV: sandbox
      JWT_SECRET: "dev_secret_change_me"
      JWT_ALG: "HS256"
    depends_on:
      - kafka

  notification-service:
    image: ${DOCKERHUB_USER}/marketplace-notification:${TAG}
    restart: unless-stopped
    ports:
      - "8005:8005"
    environment:
      KAFKA_BOOTSTRAP: kafka:29092
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    depends_on:
      - kafka
      - rabbitmq

  blockchain-service:
    image: ${DOCKERHUB_USER}/marketplace-blockchain:${TAG}
    restart: unless-stopped
    ports:
      - "8006:8006"
    environment:
      POSTGRES_URL: postgresql+asyncpg://postgres:postgres@postgres:5432/postgres
      KAFKA_BOOTSTRAP: kafka:29092
      JWT_SECRET: "dev_secret_change_me"
      JWT_ALG: "HS256"
    depends_on:
      - postgres
      - kafka

  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"

  mongo:
    image: mongo:7
    restart: unless-stopped
    ports:
      - "27017:27017"

  redis:
    image: redis:7
    restart: unless-stopped
    ports:
      - "6379:6379"

  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.1
    restart: unless-stopped
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.6.1
    restart: unless-stopped
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      # interno docker
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:29092,PLAINTEXT_HOST://0.0.0.0:9092
      # dentro de docker deben usar kafka:29092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  rabbitmq:
    image: rabbitmq:3-management
    restart: unless-stopped
    ports:
      - "5672:5672"
      - "15672:15672"
YAML

docker compose up -d
docker ps

