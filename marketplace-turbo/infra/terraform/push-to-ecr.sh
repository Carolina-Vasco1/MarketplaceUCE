#!/bin/bash
# Script para copiar imágenes de Docker Hub a AWS ECR
# Uso: ./push-to-ecr.sh <aws-region> <image-tag>

set -e

AWS_REGION=${1:-"us-east-1"}
IMAGE_TAG=${2:-"qa"}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
DOCKERHUB_USER="carovasco"

# Array de imágenes
IMAGES=(
  "marketplace-gateway"
  "marketplace-auth"
  "marketplace-product"
  "marketplace-order"
  "marketplace-payment"
  "marketplace-notification"
  "marketplace-blockchain"
  "marketplace-category"
  "marketplace-ai"
  "marketplace-admin"
  "marketplace-search"
  "marketplace-user"
  "marketplace-review"
  "marketplace-ad-connector"
  "marketplace-reporting"
)

echo "AWS Region: ${AWS_REGION}"
echo "ECR Registry: ${ECR_REGISTRY}"
echo "Image Tag: ${IMAGE_TAG}"
echo ""

# Login a ECR
echo "Logging in to AWS ECR..."
aws ecr get-login-password --region ${AWS_REGION} | \
  docker login --username AWS --password-stdin ${ECR_REGISTRY}

# Para cada imagen
for IMAGE in "${IMAGES[@]}"; do
  echo ""
  echo "Processing: ${IMAGE}:${IMAGE_TAG}"
  
  # Pull desde Docker Hub
  echo "  - Pulling from Docker Hub..."
  docker pull ${DOCKERHUB_USER}/${IMAGE}:${IMAGE_TAG} || {
    echo "  - WARNING: Image not found in Docker Hub, skipping..."
    continue
  }
  
  # Tag para ECR
  echo "  - Tagging for ECR..."
  docker tag ${DOCKERHUB_USER}/${IMAGE}:${IMAGE_TAG} \
    ${ECR_REGISTRY}/${IMAGE}:${IMAGE_TAG}
  
  # Push a ECR
  echo "  - Pushing to ECR..."
  docker push ${ECR_REGISTRY}/${IMAGE}:${IMAGE_TAG}
  
  echo "  ✓ Done!"
done

echo ""
echo "========================================="
echo "All images pushed to ECR successfully!"
echo "Registry: ${ECR_REGISTRY}"
echo "========================================="
