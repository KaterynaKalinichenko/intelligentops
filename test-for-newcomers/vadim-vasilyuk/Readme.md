# Script to run Free Tier on the AWS


## Prepare workstation

1. Set up the requirements via command:
	
	```bash
	pip install -r requirements
	```

2. Put the `config` file to the `~/.aws/` (looks like `C:\users\<your login>` in the Windows) with contents:

	```
	[default]
	region=us-east-1
	output=json
	```

3. Put the `credentials` file to the `~/.aws/` with contents:

	```
	[default]
	AWS_ACCESS_KEY_ID=<your access key>
	AWS_SECRET_ACCESS_KEY=<your secret key>
	```
The directory `~/.aws/` should look like this:
	```
	config
	credentials
	```

## Run aws resources

1. Run powershell, cmd or bash without administrator's rights

2. Change directory to current directory with script:
	
	```bash
	cd <directory with script>
	```

3. Run the command for developer:
	
	```bash
	python create_resources
	```

	> This returns private dns for local.net.

## Dispose aws resources

After using resources, important to dispose it.

1. Run the command:
	
	```bash
	python dispose_resources.py -f <file name with resources>
	```
	
	for example:
	
	```bash
	python dispose_resources.py -f sample.conf
	```
