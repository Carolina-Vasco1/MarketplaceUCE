#!/bin/bash
set -e

echo "🚀 Actualizar instancia EC2 con nuevas imágenes y configuración..."

# Crear directorio de trabajo
WORK_DIR="/opt/marketplace"
mkdir -p $WORK_DIR
cd $WORK_DIR

# Actualizar docker-compose.yml
cat > docker-compose.yml << 'EOF'
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
    image: marketplace-user:qa
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
EOF

# Actualizar nginx.conf
cat > nginx.conf << 'NGINX_EOF'
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
NGINX_EOF

echo "✅ Archivos actualizados:"
echo "   - docker-compose.yml"
echo "   - nginx.conf"

# Recrear contenedores con las nuevas imágenes
echo "🔄 Reiniciando servicios..."
docker-compose pull 2>/dev/null || echo "⚠️  Pull de algunas imágenes falló (esperado si no están en ECR)"
docker-compose down || true
docker-compose up -d

echo ""
echo "✅ Servicios iniciados!"
echo ""
echo "Esperando que los servicios estén listos..."
sleep 5

echo ""
echo "📊 Estado de los contenedores:"
docker-compose ps

echo ""
echo "🌐 URL del marketplace:"
echo "   http://marketplaceuce-qa-alb-1743538442.us-east-1.elb.amazonaws.com/"
echo ""
echo "✅ ¡Actualización completada!"
