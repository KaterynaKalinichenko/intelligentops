resource "aws_instance" "my-test-instance" {
    user_data               = "${data.template_cloudinit_config.cloudinit-example.rendered}"
    ami                     = "${var.ami_id}"
    instance_type           = "${var.instance_type}"
    count 	                = "${var.instance_count}"
    key_name        	    = "${var.key_name}"
    security_groups 	    = ["Test_SG"]

    tags {
	Name = "${var.instance_name}"
    }
}

resource "aws_security_group" "Test_SG" {
    name        = "Test_SG"
    vpc_id      = "${var.vpc_id}"

    egress {
        from_port       = 0
        to_port         = 0
        protocol        = "-1"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    ingress {
        protocol    = "tcp"
        from_port   = 22
        to_port     = 22
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow SSH"
    }

    ingress {
        protocol    = "tcp"
        from_port   = 80
        to_port     = 80
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow HTTP"
    }

    ingress {
        protocol    = "tcp"
        from_port   = 443
        to_port     = 443
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow HTTPS"
    }
}

resource "aws_key_pair" "deployer" {
    key_name   = "${var.key_name}"
    public_key = "${var.ssh_key}"
}

data "template_cloudinit_config" "cloudinit-example" {
    gzip = false
    base64_encode = true

  part {
      content_type = "text/x-shellscript"
      content = <<EOF
#!/bin/bash
sudo yum install git -y
sudo mkdir /var/repodata/
git clone https://github.com/AcalephStorage/awesome-devops /var/repodata/
    EOF
        }
}
