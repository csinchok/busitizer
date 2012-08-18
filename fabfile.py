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

def generate_reports():
    with virtualenv():
        run('coverage run manage.py test core')
        run('coverage html --include="busitizer/*" --directory=%s/webroot/coverage' % env.projectroot)
        run('pylint --rcfile=.pylintrc --output-format=html busitizer > %s/webroot/pylint.html' % env.projectroot)

def deploy():
    rsync_project(env.webroot, delete=True, exclude=['.env', '*.pyc', '.git', '.coverage', 'busitizer/webroot/static'])
    with virtualenv():
        if not files.exists('.env'):
            run('virtualenv .env')
        run('pip install -r requirements.txt')
        run('python manage.py collectstatic --noinput')
        run('supervisorctl reload')