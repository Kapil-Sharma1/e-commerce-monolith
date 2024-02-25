import os

#import boto3
#from dotenv import load_dotenv
from fabric import Connection
from fabric import task

abs_dir_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))

user = 'app'
connect_kwargs = {
    'key_filename': ['/opt/atlassian/pipelines/agent/ssh/id_rsa', ]
}

@task
def deploy_dev(ctx):
    host = '159.89.170.179'
    c = Connection(host=host, user=user, connect_kwargs=connect_kwargs)
    c.run('cd ~/nexcruise/deploy/dev && ./deploy.sh')

@task
def deploy_staging(ctx):
    host = '65.0.118.118'
    c = Connection(host=host, user=user, connect_kwargs=connect_kwargs)
    c.run('cd ~/nexcruise/deploy/staging && ./deploy.sh')
