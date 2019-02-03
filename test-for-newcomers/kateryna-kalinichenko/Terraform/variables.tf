variable "shape" {
  default = "t2.micro"
}

variable "location" {
  type = "map"

  default {
    n_virginia = "us-east-1"
    ireland    = "eu-west-1"
  }
}

variable "key_pair" {
  default = "terraform11"
}

variable "cidr_range" {
    default = "0.0.0.0/0"
  }

variable "name_prefix" {
  default = "aws_katya"
}

variable "ireland_availability_zone" {
  default = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
}