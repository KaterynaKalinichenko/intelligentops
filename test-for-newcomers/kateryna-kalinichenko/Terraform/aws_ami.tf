data "aws_ami" "test_ami" {
  most_recent = true

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "image-id"
    values = ["ami-00035f41c82244dab"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
