resource "aws_instance" "test" {
  ami                         = "${data.aws_ami.test_ami.id}"
  instance_type               = "${var.shape}"
  key_name                    = "${var.key_pair}"
  security_groups             = ["${aws_security_group.test_security_group.name}"]
  associate_public_ip_address = true

  user_data = "${file("${path.module}/templates/user_data.tpl")}"

  availability_zone = "${var.ireland_availability_zone[0]}"
}