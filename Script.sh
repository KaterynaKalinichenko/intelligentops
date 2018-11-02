#!/bin/bash

#Variables

#Credential
default_access_key=""  #Your aws access key
default_secret_key=""  #Your aws secret key
default_region=""	   #Specify region

image_id="ami-c86c3f23"    #AMI image id
instance_type="t2.micro"   #Instance type
instance_count="1"		   #How many instance your need
vpc_id=""				   #VPC id you want to use

#Install
yum update -y
yum install awscli -y

#AWSCLi Configure
aws configure set aws_access_key_id $default_access_key
aws configure set aws_secret_access_key $default_secret_key
aws configure set default.region $default_region

#Install on ec2
touch Temp.sh && chmod 777 Temp.sh
echo "#!/bin/bash" >> Temp.sh
echo "yum update -y" >> Temp.sh
echo "yum install git -y" >> Temp.sh
echo "mkdir /var/repodata/ && cd /var/repodata/ && git clone https://github.com/AcalephStorage/awesome-devops" >> Temp.sh

#ConfigureAMZ
SG_id=$(aws ec2 create-security-group --group-name SG_Test --vpc-id $vpc_id --description "Security group for Test" | awk '{ print $2 }' | sed 's/^.\(.*\).$/\1/')
aws ec2 authorize-security-group-ingress --group-name SG_Test  --protocol tcp --port 22 --cidr 0.0.0.0/0.
aws ec2 create-key-pair --key-name devenv-key --query 'KeyMaterial' --output text > devenv-key.pem
chmod 400 devenv-key.pem
aws ec2 run-instances --image-id $image_id --security-group-ids $SG_id --count $instance_count --instance-type $instance_type --key-name devenv-key --user-data file://Temp.sh

rm Temp.sh