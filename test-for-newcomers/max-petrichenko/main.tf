provider "aws" {
  region = "us-east-1"
#  access_key = "${var.aws_access_key}"
#  secret_key = "${var.aws_secret_key}"
}
resource "aws_instance" "aws_instance_creation" {

    user_data = "${data.template_cloudinit_config.userdata.rendered}"
    ami         = "${var.amiID}"
    availability_zone = "us-east-1d"
    instance_type = "t2.micro"
    key_name = "${var.ssh_key}"
}
data "template_cloudinit_config" "userdata" {
  part {
    content = <<EOF
#cloud-config
---
runcmd:
- apt-get install -y git || yum install -y git
- [ git, clone, "https://github.com/AcalephStorage/awesome-devops", "/var/repodata" ]
EOF
  }
}


    
