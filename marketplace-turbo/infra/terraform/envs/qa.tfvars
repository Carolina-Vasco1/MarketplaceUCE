project_name = "marketplaceuce-qa"
region       = "us-east-1"

key_name         = "marketplace-key"
allowed_ssh_cidr = "200.12.169.199/32"

app_port = 8000
app_image = "nginx:alpine"

# false = ASG en subnets públicas (RECOMENDADO en AWS Academy)
# true  = ASG en privadas (requiere NAT)
enable_nat = false

asg_min     = 1
asg_max     = 2
asg_desired = 1
