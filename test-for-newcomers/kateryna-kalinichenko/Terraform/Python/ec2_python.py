 #!/usr/lib/python2.7/ 
import os
import boto.ec2
ubuntu18='ami-00035f41c82244dab'
def inst(ami):
   conn = boto.ec2.connect_to_region("eu-west-1",
   aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
   aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
   conn = boto.ec2.connect_to_region("eu-west-1")
   conn.run_instances(ami,key_name='terraform11', 
   instance_type='t2.micro',
   security_groups=['aws_katya-sg'],
   user_data = '''
    #cloud-config
    packages:
     - git
    runcmd:
     - sudo git clone https://github.com/AcalephStorage/awesome-devops.git /var/repodata
    ''')

inst(ubuntu18)