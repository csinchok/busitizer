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
        run('coverage run manage.py test core --noinput')
        run('coverage html --include="busitizer/*" --directory=%s/webroot/coverage' % env.projectroot)
        with settings(warn_only=True):
            run('pylint --rcfile=.pylintrc busitizer > %s/webroot/pylint.html' % env.projectroot)

def wipe_images():
    with virtualenv():
        with settings(warn_only=True):
            run('rm webroot/media/busitized/*')
            run('rm webroot/media/originals/*')

def deploy():
    rsync_project(env.webroot, delete=True, exclude=['.env', '*.db', '*.pyc', '.git', '.coverage', 'test_images', 'busitizer/webroot/static', 'busitizer/webroot/media'])
    with virtualenv():
        if not files.exists('.env'):
            run('virtualenv .env')
        run('pip install -r requirements.txt')
        run('python manage.py collectstatic --noinput')
        run('DJANGO_SETTINGS_MODULE=busitizer.production python manage.py syncdb --noinput')
        run('DJANGO_SETTINGS_MODULE=busitizer.production python manage.py migrate')
        run('supervisorctl reload')