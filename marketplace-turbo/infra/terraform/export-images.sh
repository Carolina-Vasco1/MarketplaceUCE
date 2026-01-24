#!/bin/bash
# Script para exportar y preparar imágenes Docker para AWS EC2 sin ECR

set -e

IMAGES_DIR="/tmp/marketplace-images"
mkdir -p $IMAGES_DIR

echo "📦 Exportando imágenes Docker locales..."

# Exportar las imágenes que construimos
docker save marketplace-frontend:qa | gzip > $IMAGES_DIR/marketplace-frontend-qa.tar.gz
echo "✅ marketplace-frontend:qa exportada"

docker save marketplace-gateway:qa | gzip > $IMAGES_DIR/marketplace-gateway-qa.tar.gz
echo "✅ marketplace-gateway:qa exportada"

# Listar imágenes exportadas
echo ""
echo "📋 Imágenes disponibles en $IMAGES_DIR:"
ls -lh $IMAGES_DIR/

echo ""
echo "✅ Imágenes exportadas correctamente"
echo ""
echo "Para ejecutar en la instancia EC2:"
echo "  1. Copiar archivos .tar.gz a la instancia"
echo "  2. Ejecutar: docker load < marketplace-frontend-qa.tar.gz"
echo "  3. Ejecutar: docker load < marketplace-gateway-qa.tar.gz"
echo "  4. Ejecutar: docker-compose up -d"
