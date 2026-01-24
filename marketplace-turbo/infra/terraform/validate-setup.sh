#!/bin/bash
# Validar que todo está listo para hacer push a ECR

set -e

echo "=================================================="
echo "  Validating Marketplace ECR Setup"
echo "=================================================="
echo ""

ERRORS=0
WARNINGS=0

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_tool() {
  if ! command -v "$1" &> /dev/null; then
    echo -e "${RED}✗ ERROR: $1 not found${NC}"
    ((ERRORS++))
  else
    echo -e "${GREEN}✓ $1 found${NC}"
  fi
}

check_file() {
  if [ ! -f "$1" ]; then
    echo -e "${RED}✗ ERROR: File not found: $1${NC}"
    ((ERRORS++))
  else
    echo -e "${GREEN}✓ File exists: $1${NC}"
  fi
}

check_env() {
  if [ -z "${!1}" ]; then
    echo -e "${YELLOW}⚠ WARNING: Environment variable $1 not set${NC}"
    ((WARNINGS++))
  else
    echo -e "${GREEN}✓ $1 is set${NC}"
  fi
}

echo "1. Checking required tools..."
check_tool "docker"
check_tool "aws"
check_tool "terraform"
echo ""

echo "2. Checking Terraform files..."
check_file "main.tf"
check_file "ecr.tf"
check_file "iam.tf"
check_file "userdata.sh"
check_file "push-to-ecr.sh"
check_file "envs/qa.tfvars"
echo ""

echo "3. Checking AWS credentials..."
if aws sts get-caller-identity &> /dev/null; then
  ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
  echo -e "${GREEN}✓ AWS authenticated${NC}"
  echo "  Account ID: $ACCOUNT_ID"
else
  echo -e "${RED}✗ ERROR: AWS credentials not configured${NC}"
  ((ERRORS++))
fi
echo ""

echo "4. Checking Docker..."
if docker ps &> /dev/null; then
  echo -e "${GREEN}✓ Docker is running${NC}"
else
  echo -e "${RED}✗ ERROR: Docker is not running${NC}"
  ((ERRORS++))
fi
echo ""

echo "5. Checking Docker Hub images..."
IMAGES=(
  "marketplace-gateway"
  "marketplace-auth"
  "marketplace-product"
)

for img in "${IMAGES[@]}"; do
  if docker pull carovasco/${img}:qa &> /dev/null 2>&1; then
    echo -e "${GREEN}✓ carovasco/${img}:qa exists${NC}"
  else
    echo -e "${YELLOW}⚠ WARNING: carovasco/${img}:qa not found on Docker Hub${NC}"
    ((WARNINGS++))
  fi
done
echo ""

echo "6. Checking qa.tfvars variables..."
if grep -q "image_tag" envs/qa.tfvars; then
  echo -e "${GREEN}✓ image_tag is set${NC}"
else
  echo -e "${RED}✗ ERROR: image_tag not found in qa.tfvars${NC}"
  ((ERRORS++))
fi

if grep -q "key_name.*=.*marketplace-key" envs/qa.tfvars; then
  echo -e "${GREEN}✓ key_name is configured${NC}"
else
  echo -e "${YELLOW}⚠ WARNING: key_name might not be set correctly${NC}"
  ((WARNINGS++))
fi
echo ""

echo "7. Checking Terraform configuration..."
if terraform validate &> /dev/null; then
  echo -e "${GREEN}✓ Terraform configuration is valid${NC}"
else
  echo -e "${RED}✗ ERROR: Terraform configuration has errors${NC}"
  terraform validate
  ((ERRORS++))
fi
echo ""

echo "=================================================="
if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}✓ All checks passed!${NC}"
  if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warnings found${NC}"
  fi
else
  echo -e "${RED}✗ $ERRORS errors found${NC}"
  exit 1
fi
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. terraform apply -var-file=\"envs/qa.tfvars\""
echo "2. bash push-to-ecr.sh us-east-1 qa"
echo "3. terraform output (to see URLs)"
echo ""
