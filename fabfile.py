from fabric.api import *
from fabric.contrib.files import exists, upload_template
from fabric.contrib.project import rsync_project
import time

env.user = 'root'
env.project_name = 'boar'
env.hosts = ['137.205.98.90']
env.path = '/var/www/theboar.org'
env.version = 'current'

######################################
# Helpers
######################################

def version_path():
    return '%s/releases/%s' % (env.path, env.version)

def version(v):
    env.version = v

def wwwrun(c):
    sudo(c, user='www-data')

######################################
# Tasks
######################################

def bootstrap():
    sudo('apt-get install -y puppet rsync')

def deploy():
    require('hosts', 'path')
    
    if not exists(env.path):
        sudo('mkdir -p "%s"' % env.path)
        sudo('chown -R www-data:www-data "%s"' % env.path)
    
    version(time.strftime('%Y%m%d%H%M%S'))
    
    with cd(env.path):
        #if exists('releases/current'):
        #    wwwrun('cp -a releases/current releases/%s' % env.version)
        #else:
        wwwrun('mkdir -p releases/%s' % env.version)
        
        rsync_project(
            local_dir=".",
            remote_dir=version_path(),
            delete=True,
            extra_opts='--exclude=static_root --exclude=".git*" --exclude="*.pyc" --exclude="apache-solr-*" --exclude="*.pyc" --exclude="*~" --exclude="._*" --exclude="boar/media" --exclude=".*.swp" --exclude=".DS_Store"'
        )
    
    with cd(version_path()):
        revision = local(
            'git rev-list HEAD | head -1 | cut -c-20', 
            capture=True
        ).strip()

        upload_template('boar/settings/live.py', 'boar/settings/live.py', {
            'GIT_REVISION': revision
        })

        sudo('chown -R www-data:www-data .')
        with cd('deploy'):
            sudo('puppet --templatedir=. deps.pp')
        
        if exists('ve'):
            run('rm -rf ve')
        run('mkdir ve')
        run('virtualenv ve')
        run('pip install --upgrade -E ve -r requirements.txt', shell=True)

    manage('collectstatic --noinput')
    manage('compress')

    with cd(env.path):
        if exists('releases/previous'):
            run('rm releases/previous')
        if exists('releases/current'):
            run('mv releases/current releases/previous')
        run('ln -s %s releases/current' % version_path())

    sudo('cp %s/solr/conf/schema.xml /etc/solr/conf/schema.xml' % version_path())
    
    restart()

def restart():
    sudo('/etc/init.d/supervisor stop')
    env.warn_only = True
    while True:
        out = sudo('/etc/init.d/supervisor start')
        if not out.failed:
            break
        time.sleep(1)
    env.warn_only = False
    sudo('/etc/init.d/nginx reload')
    sudo('/etc/init.d/jetty force-reload')


def manage(c):
    with cd(version_path()):
        wwwrun('ve/bin/python boar/manage.py %s --settings=boar.settings.live' % c)
    


