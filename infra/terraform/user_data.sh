#!/bin/bash
set -e
dnf update -y
dnf install -y docker git
systemctl enable docker
systemctl start docker

# Ejemplo: clonar repo y levantar gateway+services (en prod normalmente usarías imágenes de registry)
cd /opt
git clone https://github.com/YOUR_ORG/university-marketplace.git
cd university-marketplace
docker compose up -d
