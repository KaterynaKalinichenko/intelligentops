#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mars'
import os
import sys
import boto3
import ConfigParser
import base64

"""
Usage:
python aws_ec2_creation.py PATH_TO_AWS_CREDS
Where:
  PATH_TO_AWS_CREDS - path to file that contains credentials to AWS console

Requirements:
pip install -r requirements.txt

Synopsis:
  - authentication via AWS credentials
  - verify authentication parameters
  - createaws service client
  - create EC2 security group with 22/tcp port opened
  - create EC2 instance
  - return instanceId
"""

usage_msg = '''
       Usage: python aws_ec2_creation.py PATH_TO_AWS_CREDS
         Where:
           PATH_TO_AWS_CREDS - path to file that contains credentials for AWS
'''
creds_msg = '''
       Unable to take AWS credentials from the given file.
       Please verify, that your credential file contains the following:
       [AWS_CREDENTIAL_PROFILE]
       aws_access_key_id=YOUR_ACCESS_KEY_ID
       aws_secret_access_key=YOUR_SECRET_KEY
'''

CLOUD_INIT_USERDATA = '''#cloud-config
repo_update: true
repo_upgrade: all

runcmd:
    - yum install -y git
    - mkdir /var/repodata
    - git clone https://github.com/AcalephStorage/awesome-devops.git /var/repodata/awesome-devops

output : { all : '| tee -a /var/log/cloud-init-output.log' }
'''

# DEFAULTS
AWS_CREDENTIAL_PROFILE = "ec2_manage"
AWS_REGION = "us-east-2"
AWS_EC2_INSTANCE_TYPE = "t2.micro"
AWS_EC2_INSTANCE_COUNT = 2
AWS_AMI_ID = "ami-0b59bfac6be064b78"
AWS_EC2_KEY_PAIR = "ec2_deploy"

# Default security group with SSH enabled - please change it if you have a created security group
# Create a new security group "default_sg_ssh_only" by default
AWS_EC2_DEFAULT_SEC_GROUP = "default_sg_ssh_only"


def usage(msg):
    """ Show usage information """
    print(msg)
    sys.exit(1)


def create_ec2_resource_client(aws_service, region, access_key, secret_key):
    """
    Create a resource service client by name using the default session.
    :argument aws_service: The name of a service, e.g. 's3' or 'ec2', etc
    :argument access_key: The access key to use when creating the client.
    :argument secret_key: The secret key to use when creating the client
    """
    try:
        ec2_client = boto3.resource(aws_service,
                                    region_name=region,
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key)
    except:
        print("Unable to create service client", sys.exc_info()[0])
        sys.exit(1)
    return ec2_client


def create_ec2_session_client(aws_service, region, access_key, secret_key):
    """
    Create a session client by name using the default session.
    :argument aws_service: The name of a service, e.g. 's3' or 'ec2', etc
    :argument access_key: The access key to use when creating the client.
    :argument secret_key: The secret key to use when creating the client
    """
    try:
        ec2_client = boto3.client(aws_service,
                                  region_name=region,
                                  aws_access_key_id=access_key,
                                  aws_secret_access_key=secret_key)
    except:
        print("Unable to create client", sys.exc_info()[0])
        sys.exit(1)
    return ec2_client


def create_ssh_only_security_group(resource_client, access_key, secret_key):
    """
    :param resource_client: client that can create AWS EC2 resources
    :return: security group ID
    """""
    security_group_id = False
    try:

        # Creation security group  - skip if exists
        client = create_ec2_session_client(aws_service="ec2",
                                           region=AWS_REGION,
                                           access_key=access_key,
                                           secret_key=secret_key)
        response = client.describe_security_groups()

        if len(response.get('SecurityGroups', [])):
            for i_sg in response['SecurityGroups']:
                if i_sg.get('GroupName', '') == AWS_EC2_DEFAULT_SEC_GROUP:
                    security_group_id = i_sg.get('GroupId')

        if not security_group_id:
            # Create sec group
            sec_group = resource_client.create_security_group(
                GroupName=AWS_EC2_DEFAULT_SEC_GROUP,
                Description='Default Sec Group with SSH only')
            sec_group.authorize_ingress(
                CidrIp='0.0.0.0/0',
                IpProtocol='tcp',
                FromPort=22,
                ToPort=22
            )
            security_group_id = sec_group.group_id
    except:
        pass

    return security_group_id


def main(key, secret):
    """
    :argument key:  aws_access_key_id
    :argument secret: aws_secret_access_key
    """
    # Create client that can create AWS EC2 resources
    ec2client = create_ec2_resource_client(
        aws_service="ec2", 
        region=AWS_REGION, 
        access_key=key, 
        secret_key=secret)

    # Creation security group  - skip if exists
    sec_group_id = create_ssh_only_security_group(
        ec2client,
        access_key, 
        secret_key)

    if not sec_group_id:
        print('Cannot create a security group')
        sys.exit(1)

    # Creating instance
    instances = ec2client.create_instances(
        ImageId=AWS_AMI_ID,
        MinCount=AWS_EC2_INSTANCE_COUNT,
        MaxCount=AWS_EC2_INSTANCE_COUNT,
        KeyName=AWS_EC2_KEY_PAIR,
        InstanceType=AWS_EC2_INSTANCE_TYPE,
        Monitoring={'Enabled': False},
        SecurityGroupIds=[sec_group_id],
        UserData=CLOUD_INIT_USERDATA
    )
    # Wait until instance will be ready
    for i in instances:
        i.wait_until_running()
        print("Instance successfully created! instance_id={}".format(i.instance_id))

    sys.exit()


if __name__ == '__main__':
    # Get credentials from file
    if not len(sys.argv) > 0:
        usage(usage_msg)

    # Read credentials from file
    path_to_creds = sys.argv[1]
    if not os.path.exists(path_to_creds):
        print("File with credentials didn't found. Please see usage")
        usage(usage_msg)
    else:
        config = ConfigParser.ConfigParser()
        config.read(path_to_creds)
        # setup credentials
        try:
            access_key = config.get(AWS_CREDENTIAL_PROFILE, 'aws_access_key_id')
            secret_key = config.get(AWS_CREDENTIAL_PROFILE, 'aws_secret_access_key')
            # Process of creation EC2 instance
            main(access_key, secret_key)
        except KeyError:
            usage(creds_msg)

    sys.exit()
