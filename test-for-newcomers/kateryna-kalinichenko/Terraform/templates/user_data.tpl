#cloud-config
packages:
  - git

runcmd:
  - sudo git clone https://github.com/AcalephStorage/awesome-devops.git /var/repodata

# echo "Update packages"
# sudo apt-get update -y

# echo "Instal git"
# sudo apt-get install git -y

# echo "Download repo"
# sudo git clone https://github.com/AcalephStorage/awesome-devops.git /var/repodata