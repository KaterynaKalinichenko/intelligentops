variable "access_key" {
  description = "Provide aws access key"
  default = ""
}
variable "secret_key" {
  description = "Provide aws secret key"
  default = ""
}
variable "region" {
  description = "Specify aws region"
  default = "us-east-1"
}
variable "amiID" {
  description = "Specify amiID"
  default = "ami-0ac019f4fcb7cb7e6"
}
variable "ssh_key" {
  description = "Specify ssh key"
  default = "aws_key"
}

variable "public_key" {
  description = "Specify ssh key"
  default = "aws_key.pub"
}

variable "create_key" {
  description = "Decide create key or not"
  default = ""
}



