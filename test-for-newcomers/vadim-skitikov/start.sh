#!/bin/bash
echo -e "========= | Hello ITCraft | ========="
echo ""
echo ""
chmod 777 preinstall.sh
ssh_key="itcraft.pem"
aws_key_name="itcraft"
sec_id="itcraft"
aws_image_id="ami-086a09d5b9fa35dc7"
i_type="t2.micro"
tag="Exemple"
uid=$RANDOM
count=1
region="eu-central-1"
cidr_block="10.0.0.0/28"


aws configure set region $region

#Create VPC and network
echo -e "Create VPC and network"
vpc_id=$(aws ec2 create-vpc  --cidr-block $cidr_block --query 'Vpc.VpcId' | cut -d'"' -f2)

aws ec2 modify-vpc-attribute --vpc-id $vpc_id --enable-dns-support "{\"Value\":true}"
aws ec2 modify-vpc-attribute --vpc-id $vpc_id --enable-dns-hostnames "{\"Value\":true}"

gateway_id=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' | cut -d'"' -f2)
aws ec2 attach-internet-gateway --internet-gateway-id $gateway_id --vpc-id $vpc_id

subnet_id=$(aws ec2 create-subnet --vpc-id $vpc_id --cidr-block $cidr_block --query 'Subnet.SubnetId' | cut -d'"' -f2)

route_id=$(aws ec2 create-route-table  --vpc-id $vpc_id --query 'RouteTable.RouteTableId' | cut -d'"' -f2)
aws ec2 associate-route-table  --route-table-id $route_id --subnet-id $subnet_id
aws ec2 create-route --route-table-id $route_id --destination-cidr-block 0.0.0.0/0 --gateway-id $gateway_id
aws ec2 modify-subnet-attribute --subnet-id $subnet_id --map-public-ip-on-launch

#Create secure group
echo -e "Create secure group"
security_g=$(aws ec2 create-security-group --group-name my-security-group --vpc-id $vpc_id --description "Security Group for EC2 instances to allow port 22" --query 'GroupId' | cut -d'"' -f2)
aws ec2 authorize-security-group-ingress --group-id $security_g --protocol tcp --port 22 --cidr 0.0.0.0/0

# Generate AWS Keys and store in this local box
echo -e "Generating key Pairs"
aws ec2 create-key-pair --key-name $aws_key_name --query 'KeyMaterial' --output text 2>&1 | tee $ssh_key;

#Set read only access for key
echo -e "Setting permissions"
chmod 400 $ssh_key ;

#Create instance
echo -e "Creating EC2 instance in AWS"
ec2_id=$(aws ec2 run-instances  --image-id $aws_image_id --key-name $aws_key_name --security-group-ids $security_g --subnet-id $subnet_id --instance-type $i_type --count $count --user-data file://preinstall.sh | grep InstanceId | cut -d":" -f2 | cut -d'"' -f2)

# Log date, time, random ID. This may come handy in the future for troubleshooting
date >> logs.txt
echo $aws_image_id >> logs.txt
echo $ec2_id >> logs.txt
echo $ssh_key >> logs.txt
echo ""

#echo "Unique ID: $uid"
elastic_ip=$(aws ec2 describe-instances --instance-ids $ec2_id --query 'Reservations[0].Instances[0].PublicIpAddress' | cut -d'"' -f2)
echo -e "Elastic IP: $elastic_ip"
echo $elastic_ip >> logs.txt
echo "=====" >> logs.txt
