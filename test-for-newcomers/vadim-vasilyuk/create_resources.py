
# This deploys project elit-web-api 'Free Tier' to AWS

from create_instance import create_linux_instance, wait_until_ok
from read_write import read_file, write_json
import argparse
import boto3


def arg_parser():
	parser = argparse.ArgumentParser(description='Script deploys resources on Amazon')
	parser.add_argument('-image_id', action='store', help="input the AMI's id",
						metavar="AMI's identificator", dest='image_id')
	parser.add_argument('-sg_id', action='store', help="input the security group id",
					metavar="security group identificator", dest='sg_id')
	parser.add_argument('-subnet_id', action='store', help="input the subnet id",
					metavar="subnet identificator", dest='subnet_id')
	parser.add_argument('-kp', action = 'store', help = "input the key pair",
		metavar = "key pair", dest = 'key_pair')
	arguments = parser.parse_args()
	return arguments


def main():
	arguments = arg_parser()
	linux_commands = 'linux_deploy'
	linux_image_id = arguments.image_id
	instance_type = 't2.micro'
	security_group_id = arguments.sg_id
	key_pair = arguments.key_pair
	subnet_id = arguments.subnet_id

	linux_instance = create_linux_instance(linux_image_id, read_file(linux_commands), instance_type, security_group_id,
											subnet_id, key_pair)
	wait_until_ok(linux_instance.id)

	resources = {
		'EC2_Instances': [
			{'Name': 'Linux', 'ID': linux_instance.id}
		]
	}
	write_json(resources, linux_instance.id)
	print("Linux id is: {0}".format(linux_instance.id))


if __name__ == '__main__':
	main()
