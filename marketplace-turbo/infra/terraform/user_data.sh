#!/bin/bash
set -e

# logs
exec > >(tee /var/log/user-data.log) 2>&1

yum update -y

# instalar docker
amazon-linux-extras install docker -y || true
yum install -y docker git

systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

# docker compose v2
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# clonar repo
cd /home/ec2-user
if [ -n "${GIT_REPO_URL}" ]; then
  rm -rf app || true
  git clone -b "${GIT_BRANCH}" "${GIT_REPO_URL}" app
else
  echo "GIT_REPO_URL not set. Skipping clone."
  exit 1
fi

cd /home/ec2-user/app

# levantar compose
docker compose up -d --build

docker ps
