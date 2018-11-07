
# This disposes resources aws

import boto3
import json
import os
from read_write import read_file
from create_instance import terminate_instance
import argparse


def arg_parser():
	parser = argparse.ArgumentParser(
		description='Script disposes resources on Amazon')
	parser.add_argument('-f', action='store', help="input the full path of resources",
						metavar='json file', dest='resources_file')
	arguments = parser.parse_args()
	return arguments


def main():
	file = arg_parser().resources_file
	resources = json.loads(read_file(file))
	for instance_id in resources['EC2_Instances']:
		print(instance_id['ID'])
		terminate_instance(instance_id['ID'])

	print("Removing file {0}... ".format(file), end="")
	os.remove(file)
	print('[OK]')


if __name__ == '__main__':
	main()
