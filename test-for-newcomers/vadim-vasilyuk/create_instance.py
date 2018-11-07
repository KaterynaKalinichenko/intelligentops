
# This creates and disposes EC2 instance

import boto3
ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')


def create_linux_instance(image_id, user_data, instance_type, security_grpoup_id, subnet_id, key_pair):
	print('Creating Linux instance... ', end = "")
	linux_instance = ec2.create_instances(
		BlockDeviceMappings = [
			{
				'DeviceName': '/dev/sda1',
				'VirtualName': 'ephemeral0',
				'Ebs': {
					'DeleteOnTermination': True,
					'VolumeSize': 50,
					'VolumeType': 'gp2'
				},
			},
		],
		ImageId = image_id,
		InstanceType = instance_type,
		Ipv6AddressCount = 0,
		KeyName = key_pair,
		MaxCount = 1,
		MinCount = 1,
		Monitoring = {
			'Enabled': False
		},
		SecurityGroupIds = [
			security_grpoup_id,
		],
		SubnetId = subnet_id,
		UserData = user_data,
		DisableApiTermination = False,
		DryRun = False,
		EbsOptimized = False,
		InstanceInitiatedShutdownBehavior = 'stop',
		TagSpecifications = [
			{
				'ResourceType': 'instance',
				'Tags': [
					{
						'Key': 'Project',
						'Value': 'IntelligentOps'
					},
					{
						'Key': 'Name',
						'Value': 'Free_Tier'
					}
				],
			},
			{
				'ResourceType': 'volume',
				'Tags': [
					{
						'Key': 'Project',
						'Value': 'IntelligentOps'
					},
					{
						'Key': 'Name',
						'Value': 'Free_Tier'
					}
				],
			},
		]
	)[0]
	print('[OK]')
	print(linux_instance.private_ip_address, linux_instance.id)
	return linux_instance


def wait_until_ok(instance_id):
	print('Wait until instance initialise...', end = "")
	waiter = ec2_client.get_waiter('instance_status_ok')
	waiter.wait(
		InstanceIds = [instance_id],
		WaiterConfig = {
			'Delay': 30,
			'MaxAttempts': 50
		}
	)
	print('[OK]')


def terminate_instance(instance_id):
	instance = ec2.Instance(instance_id)
	print('Removing instance {0}... '.format([tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'][0]), end = "")
	instance.terminate()
	instance.wait_until_terminated()
	print('[OK]')
