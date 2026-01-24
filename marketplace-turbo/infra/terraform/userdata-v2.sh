#!/bin/bash
set +e
exec >> /var/log/userdata.log 2>&1
echo "=== Marketplace Full Stack Deployment START ==="

# Install dependencies
dnf install -y docker curl git awscli python3 postgresql-client git &
INSTALL_PID=$!
systemctl start docker
sleep 2
wait $INSTALL_PID 2>/dev/null

# Install Docker Compose
mkdir -p /usr/local/lib/docker/cli-plugins
curl -s -L https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose 2>/dev/null
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Create working directory
mkdir -p /opt/marketplace
cd /opt/marketplace

# Clone or download the repository (using git clone)
git clone https://github.com/your-repo/marketplace.git . 2>/dev/null || echo "Git clone failed, continuing with manual setup"

# Create docker-compose.yml
cat > docker-compose.yml << 'COMPOSE'
version: '3.8'

services:
  frontend:
    image: marketplace-frontend:qa
    container_name: marketplace-frontend
    expose:
      - "3000"
    environment:
      - VITE_API_URL=http://gateway:8000
    restart: always
    networks:
      - marketplace-network

  gateway:
    image: marketplace-gateway:qa
    container_name: marketplace-gateway
    expose:
      - "8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
    depends_on:
      - postgres
      - redis
    networks:
      - marketplace-network

  auth-service:
    image: marketplace-auth:qa
    container_name: marketplace-auth
    expose:
      - "8001"
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
    depends_on:
      - postgres
    networks:
      - marketplace-network

  product-service:
    image: marketplace-product:qa
    container_name: marketplace-product
    expose:
      - "8002"
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
    depends_on:
      - postgres
      - mongo
    networks:
      - marketplace-network

  order-service:
    image: marketplace-order:qa
    container_name: marketplace-order
    expose:
      - "8003"
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
    depends_on:
      - postgres
      - rabbitmq
    networks:
      - marketplace-network

  payment-service:
    image: marketplace-payment:qa
    container_name: marketplace-payment
    expose:
      - "8004"
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
    depends_on:
      - postgres
    networks:
      - marketplace-network

  notification-service:
    image: marketplace-notification:qa
    container_name: marketplace-notification
    expose:
      - "8005"
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
    depends_on:
      - rabbitmq
    networks:
      - marketplace-network

  blockchain-service:
    image: marketplace-blockchain:qa
    container_name: marketplace-blockchain
    expose:
      - "8006"
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
    depends_on:
      - postgres
    networks:
      - marketplace-network

  postgres:
    image: postgres:16
    container_name: marketplace-postgres
    environment:
      POSTGRES_DB: marketplace
      POSTGRES_USER: marketplace
      POSTGRES_PASSWORD: marketplace_password_123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    expose:
      - "5432"
    restart: always
    networks:
      - marketplace-network

  mongo:
    image: mongo:7
    container_name: marketplace-mongo
    environment:
      MONGO_INITDB_DATABASE: marketplace
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin_password_123
    volumes:
      - mongo_data:/data/db
    expose:
      - "27017"
    restart: always
    networks:
      - marketplace-network

  redis:
    image: redis:7
    container_name: marketplace-redis
    expose:
      - "6379"
    restart: always
    networks:
      - marketplace-network

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    expose:
      - "2181"
    restart: always
    networks:
      - marketplace-network

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    expose:
      - "9092"
    restart: always
    networks:
      - marketplace-network

  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    container_name: marketplace-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin_password_123
    expose:
      - "5672"
      - "15672"
    restart: always
    networks:
      - marketplace-network

  prometheus:
    image: prom/prometheus:latest
    container_name: marketplace-prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    expose:
      - "9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    restart: always
    networks:
      - marketplace-network

  grafana:
    image: grafana/grafana:latest
    container_name: marketplace-grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    expose:
      - "3001"
    volumes:
      - grafana_data:/var/lib/grafana
    restart: always
    networks:
      - marketplace-network

  nginx:
    image: nginx:alpine
    container_name: marketplace-nginx
    ports:
      - "80:80"
      - "8000:8000"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - frontend
      - gateway
    restart: always
    networks:
      - marketplace-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  marketplace-network:
    driver: bridge

volumes:
  postgres_data:
  mongo_data:
  prometheus_data:
  grafana_data:
COMPOSE

# Create nginx.conf
cat > nginx.conf << 'NGINX_CONF'
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
NGINX_CONF

# Create prometheus.yml
cat > prometheus.yml << 'PROMETHEUS'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'gateway'
    static_configs:
      - targets: ['gateway:8000']
PROMETHEUS

# Start Docker daemon
systemctl enable docker
systemctl start docker
sleep 2

# Pull and run services
docker-compose pull 2>/dev/null || echo "Pull failed, will use local images if available"
docker-compose down 2>/dev/null || true
docker-compose up -d

# Wait for services to stabilize
sleep 10

# Show status
docker-compose ps

echo "=== Marketplace Full Stack Deployment COMPLETE ==="
echo "Frontend will be available at: http://<ALB-DNS>/health"
echo "Health check: http://<ALB-DNS>/health"
