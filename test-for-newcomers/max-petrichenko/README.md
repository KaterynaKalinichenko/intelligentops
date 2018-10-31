To perform instance creation you should use the following instructions:

1. Install Terraform on the server/local pc. Quick guide for your convenience:
https://www.terraform.io/intro/getting-started/install.html

2. Copy manifests to any folder and run the following commands in the terminal/console:

terraform init 
terraform apply

Supply two variables interactively:

amiID - example with Ubuntu: ami-0ac019f4fcb7cb7e6
ssh_key - a name of ssh key in aws (assume that you created it already)

NOTE:
Running Terraform assumes that you installed aws secret/public keys at default location depending on OS.

In case you haven't installed it yet, "uncomment" code in both files and supply them as variables.
