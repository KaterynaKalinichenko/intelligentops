resource "aws_security_group" "test_security_group" {
  name        = "${var.name_prefix}-sg"
  description = "test security group"
  vpc_id      = "${aws_default_vpc.test_vpc.id}"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.cidr_range}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["${var.cidr_range}"]
  }
}
