## Hello there! :)

If you came here from the job interview - welcome, we've been waiting for you! But if you came here by chance, please do not hesitate to do the task too :-)

## Conditions
1. The result of the task is a file or directory with a solution, named by your first name and last name, e.g. 'thomas-anderson'.
2. Solution be added to 'intelligentops/test-for-newcomers/' (this repository/folder) via "Pull Request" function.
3. Description of the task

    Use your favorite scripting language (bash, python, etc...) to script the process of EC2 instance creation from AMI. This instance should automatically pull a content of certain third-party repository at launch and place it into '/var/repodata' directory.
    
    Please follow this guidance in your work:
    
        - 'at launch' action inside instance must be performed using cloud-init (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
        - AMI ID must be supplied to the script as a variable and AMI itself must be labeled as 'Free Tier' in AMI marketplace, so we could use it to validate your results 
        - Repository for the test is https://github.com/AcalephStorage/awesome-devops

