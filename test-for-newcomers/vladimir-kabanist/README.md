## A command line utility which creates an instance according to the task requirements

Some additional features present. For detailed information about the script capabilities use help: `./aws_instance.py -h`

The script will try to locate AWS credentials automatically at default locations. 
If you don't have them, access and secret keys need to be passed as command line arguments.

## Requirements

The script requires python3 and boto3 library.
If you already have python3 and pip installed simply run:

`pip3 install -r requirements.txt`

If you don't have either python3 or pip installed - please refer to official install guides for your OS distribution.

## Important notes:

- If you specify the region different from `us-east-1` you will also need to supply a valid AMI ID, since they are region-specific.
- When you specify security groups - please make sure that you use the group name, not ID. Attemts to use security group ID instead of name will cause errors.
- If you have different aws profiles configured on your system, you can specify the profile name with `--config-profile` command line argument.


