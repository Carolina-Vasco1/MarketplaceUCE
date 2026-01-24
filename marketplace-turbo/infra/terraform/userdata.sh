#!/bin/bash
set +e
exec >> /var/log/userdata.log 2>&1
echo "=== Marketplace Full Stack Deployment START ==="

# Install dependencies
dnf install -y docker curl git awscli python3 postgresql-client &
INSTALL_PID=$!
systemctl start docker &
sleep 5
wait $INSTALL_PID 2>/dev/null

# ECR Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 243912447778.dkr.ecr.us-east-1.amazonaws.com 2>/dev/null || true

# Install Docker Compose
mkdir -p /usr/local/lib/docker/cli-plugins
curl -s -L https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose 2>/dev/null
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Create docker-compose.yml with complete marketplace stack
mkdir -p /opt/marketplace
cd /opt/marketplace

cat > docker-compose.yml <<'COMPOSE'
version: '3.8'

services:
  # =========================
  # FRONTEND
  # =========================
  frontend:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-frontend:qa
    environment:
      VITE_API_URL: http://gateway:8000
    restart: unless-stopped
    expose:
      - "3000"

  # =========================
  # API GATEWAY
  # =========================
  gateway:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-gateway:qa
    expose:
      - "8000"
    environment:
      JWT_SECRET: dev_secret_change_me
      JWT_ALG: HS256
      FRONTEND_ORIGIN: "*"
      AUTH_URL: http://auth-service:8001
      PRODUCT_URL: http://product-service:8002
      ORDER_URL: http://order-service:8003
      PAYMENT_URL: http://payment-service:8004
      NOTIF_URL: http://notification-service:8005
      BLOCKCHAIN_URL: http://blockchain-service:8006
    depends_on:
      - postgres
      - redis
      - auth-service
      - product-service
      - order-service
      - payment-service
      - notification-service
      - blockchain-service
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  # =========================
  # MICROSERVICES
  # =========================
  auth-service:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-auth:qa
    expose:
      - "8001"
    environment:
      DATABASE_URL: postgresql://auth:auth@postgres:5432/auth_db
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET: dev_secret_change_me
      JWT_ALG: HS256
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  product-service:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-product:qa
    expose:
      - "8002"
    environment:
      JWT_SECRET: dev_secret_change_me
      JWT_ALG: HS256
      MONGO_URL: mongodb://mongo:27017
      MONGO_DB: marketplaceUce
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - mongo
      - redis
    restart: unless-stopped

  order-service:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-order:qa
    expose:
      - "8003"
    environment:
      DATABASE_URL: postgresql://order:order@postgres:5432/order_db
      KAFKA_BOOTSTRAP: kafka:29092
      JWT_SECRET: dev_secret_change_me
      JWT_ALG: HS256
    depends_on:
      - postgres
      - kafka
    restart: unless-stopped

  payment-service:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-payment:qa
    expose:
      - "8004"
    environment:
      KAFKA_BOOTSTRAP: kafka:29092
      PAYPAL_ENV: sandbox
      JWT_SECRET: dev_secret_change_me
      JWT_ALG: HS256
    depends_on:
      - kafka
    restart: unless-stopped

  notification-service:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-notification:qa
    expose:
      - "8005"
    environment:
      KAFKA_BOOTSTRAP: kafka:29092
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
      SMTP_HOST: smtp.gmail.com
      SMTP_PORT: 587
    depends_on:
      - kafka
      - rabbitmq
    restart: unless-stopped

  blockchain-service:
    image: 243912447778.dkr.ecr.us-east-1.amazonaws.com/marketplace-user:qa
    expose:
      - "8006"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/postgres
      KAFKA_BOOTSTRAP: kafka:29092
      JWT_SECRET: dev_secret_change_me
      JWT_ALG: HS256
    depends_on:
      - postgres
      - kafka
    restart: unless-stopped

  # =========================
  # DATABASES
  # =========================
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_INITDB_ARGS: "-c max_connections=200"
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 30
    restart: unless-stopped

  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongodata:/data/db
    healthcheck:
      test: ["CMD-SHELL", "mongosh --eval \"db.adminCommand('ping')\" --quiet || exit 1"]
      interval: 5s
      timeout: 10s
      retries: 30
    restart: unless-stopped

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 30
    restart: unless-stopped

  # =========================
  # MESSAGE QUEUES & STREAMING
  # =========================
  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.1
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"
    restart: unless-stopped

  kafka:
    image: confluentinc/cp-kafka:7.6.1
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:29092,PLAINTEXT_HOST://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    healthcheck:
      test: ["CMD-SHELL", "kafka-broker-api-versions --bootstrap-server localhost:29092 >/dev/null 2>&1 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 25
    restart: unless-stopped

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    restart: unless-stopped

  # =========================
  # MONITORING
  # =========================
  prometheus:
    image: prom/prometheus:v2.55.0
    ports:
      - "9090:9090"
    volumes:
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:11.2.0
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_USERS_ALLOW_SIGN_UP: "false"
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

  # =========================
  # REVERSE PROXY
  # =========================
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "8000:8000"
    volumes:
      - /opt/marketplace/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - gateway
      - frontend
    restart: unless-stopped

volumes:
  pgdata:
  mongodata:
  prometheus_data:
  grafana_data:

networks:
  default:
    driver: bridge
COMPOSE

# Create nginx configuration
cat > nginx.conf <<'NGINX'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    upstream frontend {
        server frontend:3000;
    }

    upstream gateway {
        server gateway:8000;
    }

    server {
        listen 80 default_server;
        listen 8000 default_server;
        server_name _;
        client_max_body_size 100M;

        # API routes - PRIORITY (must be first)
        location ~ ^/api/ {
            proxy_pass http://gateway;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Health check endpoint for ALB
        location ~ ^/health$ {
            proxy_pass http://gateway/health;
            proxy_set_header Host $host;
            access_log off;
        }

        # Frontend - SPA with fallback to index.html
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            
            # Error page handling for SPA
            proxy_intercept_errors on;
            error_page 404 /index.html;
        }
    }
}
NGINX

echo "=== Pulling Docker images ==="
timeout 600 docker-compose pull --quiet 2>/dev/null || echo "Warning: Some images may need to be built locally"

echo "=== Starting all services ==="
docker-compose up -d 2>&1

# Wait for services
echo "=== Waiting 60 seconds for services to stabilize ==="
sleep 60

echo "=== Services Status ==="
docker ps --no-trunc
echo ""
echo "=== Docker Compose Logs ==="
docker-compose logs --tail=20

echo "=== Full Stack Deployment COMPLETE ==="
echo "Access marketplace at: http://localhost or http://localhost:8000"
