provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
}
resource "aws_instance" "aws_instance_creation" {
    user_data = "${data.template_cloudinit_config.userdata.rendered}"
    ami       = "${var.amiID}"
    availability_zone = "us-east-1d"
    instance_type = "t2.micro"
    key_name = "${var.ssh_key}"  

    tags {
    Name =  "Test-instance"  
  } 
}

resource "aws_key_pair" "ec2key" {
  key_name = "${var.ssh_key}" 
  count = "${var.create_key == "create" ? 1 : 0}"
  public_key = "${file("${var.public_key}")}"
}

data "template_cloudinit_config" "userdata" {
  part {
    content = <<EOF
#cloud-config
---
repo_update: true
repo_upgrade: all

packages:
    - git

runcmd:   
- [ git, clone, "https://github.com/AcalephStorage/awesome-devops", "/var/repodata" ]
EOF
  }
}

output "public_ip" {
  value = ["${aws_instance.aws_instance_creation.*.public_ip}"]
}