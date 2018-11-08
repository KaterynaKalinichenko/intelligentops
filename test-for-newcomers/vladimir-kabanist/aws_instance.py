#!/usr/bin/env python3

import uuid
import boto3
import botocore
import argparse

argument_parser = argparse.ArgumentParser(description="Create ec2 instance with userdata for ITC test task")
argument_parser.add_argument('--access_key', help='AWS access key')
argument_parser.add_argument('--secret_key', help='AWS secret key')
argument_parser.add_argument('--region', help='AWS region (us-east-1 by default)', default='us-east-1')
argument_parser.add_argument('--keypair', help='EC2 key pair name')
argument_parser.add_argument('--ami_id', help='Server image ID (ami-0ff8a91507f77f867 by default)', default='ami-0ff8a91507f77f867')
argument_parser.add_argument('--instance_type', help='EC2 instance type (t3.micro by default)', default='t3.micro')
argument_parser.add_argument('--sg', help='Security group that needs to be attached to the instance', nargs='*')
argument_parser.add_argument('--config_profile', help='The name of AWS config profile')


def create_aws_session(args):
    session = boto3.Session(region_name=args.region,
                            aws_access_key_id=args.access_key,
                            aws_secret_access_key=args.secret_key,
                            profile_name=args.config_profile)
    if session.get_credentials() is None:
        print('Credentials were not found at default locations.\n'
              'Please specify "--aws_access_key" and "--aws_secret_key" explicitly.\n'
              'For more info on script usage use -h or --help flag')
        exit(1)

    return session


def create_new_key_pair(args, session):
    try:
        ec2 = session.resource('ec2')
        random_key_name = uuid.uuid4().hex
        key_pair = ec2.create_key_pair(KeyName=random_key_name)

        print(key_pair.key_material)
        args.keypair = key_pair.key_name

    except botocore.exceptions.ClientError as error:
        print(error)
        exit(1)


def create_new_security_group(args, session):
    try:
        ec2 = session.resource('ec2')
        random_sg_name = uuid.uuid4().hex
        sg = ec2.create_security_group(GroupName=random_sg_name,
                                       Description='SG for ssh access')
        sg.authorize_ingress(CidrIp='0.0.0.0/0',
                             FromPort=22,
                             ToPort=22,
                             IpProtocol='tcp'
                             )
        args.sg = [sg.group_name]

    except botocore.exceptions.ClientError as error:
        print(error)
        exit(1)


def create_instance(args, session):
    try:
        ec2 = session.resource('ec2')
        userdata_file = open('user-data.cloudinit', 'r')
        userdata_text = userdata_file.read().strip()
        userdata_file.close()
        ec2_instance = ec2.create_instances(ImageId=args.ami_id,
                             InstanceType=args.instance_type,
                             KeyName=args.keypair,
                             SecurityGroups=args.sg,
                             UserData=userdata_text,
                             MinCount=1,
                             MaxCount=1)

        print('Waiting for an instance to be in "running" state.....\n')
        ec2_instance[0].wait_until_running()
        ec2_instance[0].load()

        return ec2_instance[0]

    except botocore.exceptions.ClientError as error:
        print(error)
        exit(1)
    except FileNotFoundError as error:
        print('ERROR: The file with userdata was not found\n'
              'Please make sure that the file "userdata.cloudinit" is present in the same directory as this script\n')
        exit(1)


def display_summary(args):
    new_keypair_message = 'NEW keypair with a random name'
    new_sg_message = 'NEW security grout with a random name which allows SSH access from any IP'
    summary_message = f"The script is about to create NEW EC2 instance in {args.region} region, with:\n" \
                      f"    type: {args.instance_type}\n" \
                      f"    ami_id: {args.ami_id}\n" \
                      f"    keypair: {new_keypair_message if args.keypair is None else args.keypair}\n" \
                      f"    security_groups: {new_sg_message if args.sg is None else args.sg}\n"
    print(summary_message)


if __name__ == '__main__':
    args = argument_parser.parse_args()
    session = create_aws_session(args)

    display_summary(args)
    user_confirmation = input('Please confirm resources creation by typing "Y" or "Yes"\n')

    if user_confirmation.strip().lower() == 'y' or user_confirmation.strip().lower() == 'yes':
        print('Operation confirmed, proceeding....\n')
    else:
        print('Confirmation was not submitted, aborting')
        exit(0)

    if args.keypair is None:
        create_new_key_pair(args,session)

    if args.sg is None:
        create_new_security_group(args,session)

    ec2_instance = create_instance(args, session)

    print('EC2 instance has been created\n'
          'Instance details:\n'
          f'id - {ec2_instance.instance_id}\n'
          f'public ip - {ec2_instance.public_ip_address}\n'
          f'type - {ec2_instance.instance_type}\n'
          f'dns name - {ec2_instance.public_dns_name}\n'
          f'key name - {ec2_instance.key_name}\n')

