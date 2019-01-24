#!/bin/bash
private_key=MyKey1.pem
public_key=MyKey1
instance_type=t2.micro
region="us-west-2"

aws configure set region $region

aws ec2 create-key-pair \
	--key-name $public_key \
	--query "KeyMaterial" \
	--output text > $private_key

if [ $? -eq 0 ]; then echo The SSH cryptographic key pair have been created.; fi

vcp_id=$(aws ec2 create-default-vpc --query 'Vpc.VpcId' | cut -d '"' -f2)

security_group_id=$(aws ec2 describe-security-groups --query "SecurityGroups[*].{Name:GroupId}" | cut -d '"' -f 4 -s)

aws ec2 authorize-security-group-ingress --group-id $security_group_id --protocol tcp --port 22 --cidr 0.0.0.0/0

resultName=$(aws ec2 run-instances \
	--image-id $1 \
	--security-group-ids $security_group_id \
	--user-data file://user_data.txt \
	--count 1 \
	--instance-type $instance_type \
	--key-name $public_key \
	--query "Instances[0].InstanceId")

instance_name=$(echo $resultName | tr -d \")

if [ $? -eq 0 ]; then echo "Instance $instance_name has been created." ; fi

resultIP=$(aws ec2 describe-instances \
	--instance-ids $instance_name \
	--query "Reservations[0].Instances[0].PublicIpAddress")

instance_ip=$(echo $resultIP| tr -d \")
echo IP address is $instance_ip

#Connect to the instance
#ssh -i MyKey1.pem ec2-user@$instance_ip
