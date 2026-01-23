project_name     = "marketplaceuce-qa"
region           = "us-east-1"

key_name         = "marketplace-key"
allowed_ssh_cidr = "157.100.202.206/32"

app_port = 8000

dockerhub_user = "carovasco"
image_tag      = "qa"

enable_nat  = false
asg_min     = 1
asg_max     = 2
asg_desired = 1
