import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files

from contextlib import contextmanager as _contextmanager

env.hosts = ['66.175.213.211']
env.user = 'fabric'
env.webroot = '/www/'
env.projectroot = os.path.join(env.webroot, 'busitizer')
env.activate = 'source .env/bin/activate'

@_contextmanager
def virtualenv():
    with cd(env.projectroot):
        with prefix(env.activate):
            yield

def deploy():
    rsync_project(env.webroot, delete=True, exclude=['.env', '*.pyc', '.git', 'busitizer/webroot/static'])
    with virtualenv():
        if not files.exists('.env'):
            run('virtualenv .env')
        run('pip install -r requirements.txt')
        run('python manage.py collectstatic --noinput')
        run('supervisorctl reload')