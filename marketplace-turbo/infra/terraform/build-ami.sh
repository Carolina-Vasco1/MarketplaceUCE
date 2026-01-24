#!/bin/bash
###########################
# Build Custom Marketplace AMI
# This script creates an AMI with Docker and preloaded images
###########################

set -e

echo "=========================================="
echo "🔨 Building Marketplace AMI"
echo "=========================================="

# Configuration
REGION="${AWS_REGION:-us-east-1}"
KEY_NAME="${1:-marketplace-key}"
KEY_PATH="${2:-./marketplace-key.pem}"
INSTANCE_TYPE="t3.micro"
AMI_NAME="marketplace-ami-$(date +%s)"
TAG="qa"

# Get latest Amazon Linux 2023 AMI
echo "🔍 Fetching Amazon Linux 2023 AMI ID..."
BASE_AMI=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-*" "Name=state,Values=available" \
  --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
  --output text \
  --region "$REGION")

echo "   Using base AMI: $BASE_AMI"

# Create VPC if needed
echo "🌐 Checking VPC configuration..."
VPC_ID=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text --region "$REGION")
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[0].SubnetId' --output text --region "$REGION")
SG_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" --query 'SecurityGroups[0].GroupId' --output text --region "$REGION")

if [ "$SG_ID" = "None" ] || [ -z "$SG_ID" ]; then
  echo "   Creating security group..."
  SG_ID=$(aws ec2 create-security-group \
    --group-name marketplace-ami-builder \
    --description "For building marketplace AMI" \
    --vpc-id "$VPC_ID" \
    --region "$REGION" \
    --query 'GroupId' \
    --output text)
  
  aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp --port 22 \
    --cidr 0.0.0.0/0 \
    --region "$REGION"
else
  echo "   Using existing SG: $SG_ID"
fi

# Create IAM instance profile for builder (simple, no permissions needed)
echo "👤 Creating IAM instance profile..."
PROFILE_NAME="marketplace-ami-builder-$(date +%s)"

cat > /tmp/trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

ROLE_NAME="marketplace-builder-role-$(date +%s)"
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file:///tmp/trust-policy.json \
  --region "$REGION" 2>/dev/null || true

aws iam create-instance-profile \
  --instance-profile-name "$PROFILE_NAME" \
  --region "$REGION" 2>/dev/null || true

aws iam add-role-to-instance-profile \
  --instance-profile-name "$PROFILE_NAME" \
  --role-name "$ROLE_NAME" \
  --region "$REGION" 2>/dev/null || true

echo "   Profile: $PROFILE_NAME"

# Create builder instance
echo "🚀 Launching builder instance..."

cat > /tmp/userdata.sh << 'USERDATA'
#!/bin/bash
set -ex
exec > /tmp/userdata.log 2>&1

echo "=== Starting AMI build ===" 

# Update and install Docker
yum update -y
yum install -y docker git curl wget

# Start Docker daemon
systemctl start docker
systemctl enable docker

# Download and install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Pull base images
echo "Pulling Docker images..."
docker pull postgres:15 &
docker pull redis:7 &
docker pull nginx:latest &
wait

# Pull marketplace images (will fail if not in ECR, that's ok)
ECR_REGISTRY="YOUR_ECR_REGISTRY"
IMAGE_TAG="qa"

docker pull "$ECR_REGISTRY/marketplace-gateway:$IMAGE_TAG" 2>/dev/null || echo "Gateway image not available yet"
docker pull "$ECR_REGISTRY/marketplace-auth-service:$IMAGE_TAG" 2>/dev/null || echo "Auth service not available yet"
docker pull "$ECR_REGISTRY/marketplace-product-service:$IMAGE_TAG" 2>/dev/null || echo "Product service not available yet"
docker pull "$ECR_REGISTRY/marketplace-order-service:$IMAGE_TAG" 2>/dev/null || echo "Order service not available yet"
docker pull "$ECR_REGISTRY/marketplace-payment-service:$IMAGE_TAG" 2>/dev/null || echo "Payment service not available yet"
docker pull "$ECR_REGISTRY/marketplace-notification-service:$IMAGE_TAG" 2>/dev/null || echo "Notification service not available yet"
docker pull "$ECR_REGISTRY/marketplace-blockchain-service:$IMAGE_TAG" 2>/dev/null || echo "Blockchain service not available yet"
docker pull "$ECR_REGISTRY/marketplace-frontend:$IMAGE_TAG" 2>/dev/null || echo "Frontend not available yet"

echo "=== AMI build complete ==="
touch /tmp/build-complete
USERDATA

INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$BASE_AMI" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --subnet-id "$SUBNET_ID" \
  --security-group-ids "$SG_ID" \
  --user-data file:///tmp/userdata.sh \
  --associate-public-ip-address \
  --iam-instance-profile "Name=$PROFILE_NAME" \
  --region "$REGION" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$AMI_NAME-builder}]" \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "   Instance ID: $INSTANCE_ID"

# Wait for instance running
echo "⏳ Waiting for instance to start..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID" --region "$REGION"

# Get public IP
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text \
  --region "$REGION")

echo "   Public IP: $INSTANCE_IP"

# Wait for SSH availability
echo "⏳ Waiting for SSH (max 60s)..."
for i in {1..12}; do
  if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i "$KEY_PATH" ec2-user@"$INSTANCE_IP" "test -f /tmp/build-complete" 2>/dev/null; then
    echo "   ✓ Build complete!"
    break
  fi
  echo "   Attempt $i/12..."
  sleep 5
done

# Create AMI from instance
echo "📸 Creating AMI from instance..."
IMAGE_ID=$(aws ec2 create-image \
  --instance-id "$INSTANCE_ID" \
  --name "$AMI_NAME" \
  --description "Marketplace AMI with Docker and preloaded images" \
  --region "$REGION" \
  --query 'ImageId' \
  --output text)

echo "   AMI ID: $IMAGE_ID"
echo "   Waiting for AMI creation..."
aws ec2 wait image-available --image-ids "$IMAGE_ID" --region "$REGION"

# Tag the AMI
aws ec2 create-tags \
  --resources "$IMAGE_ID" \
  --tags Key=Name,Value="$AMI_NAME" \
  --region "$REGION"

# Terminate builder instance
echo "🧹 Cleaning up builder instance..."
aws ec2 terminate-instances --instance-ids "$INSTANCE_ID" --region "$REGION"

# Output results
echo ""
echo "=========================================="
echo "✅ AMI Build Complete!"
echo "=========================================="
echo "AMI ID: $IMAGE_ID"
echo "AMI Name: $AMI_NAME"
echo ""
echo "To use this AMI in Terraform:"
echo "  Update your launch template with: image_id = \"$IMAGE_ID\""
echo ""
