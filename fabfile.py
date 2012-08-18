import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files

env.hosts = ['66.175.213.211']
env.user = 'fabric'
env.webroot = '/www/'

def deploy():
    rsync_project(env.webroot, delete=True, exclude=['.env', '*.pyc', '.git'])
    with cd(os.path.join(env.webroot, 'busitizer')):
        if not files.exists('.env'):
            run('virtualenv .env')
        run('pip install -r requirements.txt')