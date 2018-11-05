# AWS Config

variable "aws_access_key" {
    default = "" #Specify your aws access key
}
  
variable "aws_secret_key" {
    default = "" #Specify your aws secret key
}

variable "aws_region" {
    default = "" #Specify region of instances location (for example eu-central-1)
}

variable "instance_name" {
    default = "" #Specify instance name
}

variable "ami_id" {
    default = "" #Specify AMI id (for example ami-c86c3f23)
}

variable "instance_type" {
    default = "" #Specify instance type (for example t2.micro)
}

variable "vpc_id" {
    default = "" #Specify your VPC id
}

variable "instance_count" {
    default = "" #Specify how many instances you need
}

variable "key_name" {
    default = "" #Specify your ssh key name
}

variable "ssh_key" {
    default = "" #Specify your ssh key
}
