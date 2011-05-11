from __future__ import with_statement
from fabric.api import *
from fabric.contrib.files import exists
import sys
import time


env.project_name = 'boar'
env.roledefs = {
    'localhost': ['127.0.0.1',],
    'live': ['mew.theboar.org',],
}
 
######################################
# Environment
######################################
 
def localhost():
    """
    Set up a development environment locally.
    """
    env.hosts = env.roledefs['localhost']
    env.path = '/'.join(sys.modules[__name__].__file__.split('/')[:-1])
    env.version_path = env.path

def live():
    env.hosts = env.roledefs['live']
    env.path = '/var/www/theboar.org'

######################################
# Tasks
######################################

def management_command(c):
    require('path', 'version_path')
    with cd(env.version_path):
        with cd(env.project_name):
            run('./manage.py %s --settings=configs.live.settings' % c)
    
def test():
    "Run the test suite and bail out if it fails"
    management_command('test --noinput accounts articles cacher common search uploads')

def syncdb_migrate():
    management_command('syncdb')
    management_command('migrate')

def rebuild_index():
    sudo('/etc/init.d/tomcat5.5 restart')
    management_command('rebuild_index --noinput')


@runs_once
def setup():
    require('hosts', 'path')
    
    sudo('apt-get install -y csstidy python-cairo python-cjson python-imaging python-psycopg2')
    # GeoDjango
    sudo('apt-get install -y libgeos-3.0.0 proj postgis gdal-bin postgresql-8.3-postgis')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    with cd(env.path):
        run('mkdir -p packages')
        run('mkdir -p releases')

def version(version):
    env.version = version
    env.version_path = '%s/releases/%s' % (env.path, env.version)

def create_version():
    require('hosts', 'path')
    version(time.strftime('%Y%m%d%H%M%S'))
    
    with cd(env.path):
        run('mkdir -p releases/%s' % env.version)
    
    upload_tar_from_git()
    setup_virtualenv()
    install_requirements()

def deploy():
    "Specify a specific version to be made live"
    require('hosts', 'path', 'version')
    
    with cd(env.path):
        if exists('releases/previous'):
            run('rm releases/previous')
        if exists('releases/current'):
            run('mv releases/current releases/previous')
        run('ln -s %s releases/current' % env.version_path)
    
    # lol, solr hacks
    sudo('cp %(version_path)s/solr/conf/schema.xml /etc/solr/conf/schema.xml' % env)
    
    run('rm -f %(path)s/media/static' % env)
    run('ln -s %(version_path)s/boar/media/static %(path)s/media/static' % env)
    run('rm -f %(path)s/media/admin' % env)
    run('ln -s %(version_path)s/boar_ve/lib/python2.5/site-packages/django/contrib/admin/media %(path)s/media/admin' % env)
    
    restart_apache()
    restart_celery()
    
def setup_virtualenv():
    require('version_path')
    
    with cd(env.version_path):
        run('mkdir -p %s_ve' % env.project_name)
        run('virtualenv %s_ve/' % env.project_name)

def upload_tar_from_git():
    "Create an archive from the current Git master branch and upload it"
    require('version', 'path')
    
    local('git archive --format=tar master | gzip > %s.tar.gz' % env.version)
    with cd(env.path):
        run('mkdir -p releases/%s' % env.version)
        put('%s.tar.gz' % env.version, '%s/packages/' % env.path)
        with cd('releases/%s' % env.version):
            run('tar zxf ../../packages/%s.tar.gz' % env.version)
    local('rm %s.tar.gz' % env.version)

def install_requirements():
    "Install the required packages from the requirements file using pip"
    require('version_path')
    with cd(env.version_path):
        run('pip install --upgrade -E %s_ve/ -r requirements.txt' % env.project_name)

def restart_apache():
    sudo('/etc/init.d/apache2 restart')

def restart_celery():
    sudo('/etc/init.d/celeryd restart')
    sudo('/etc/init.d/celerybeat restart')

def setup_dev():
    require('version_path')
    setup()
    setup_virtualenv()
    install_requirements()

def clean():
    local("find ./%s/ -name '*.pyc' -exec rm -rf {} \;" % env.project_name)

def generate_fixtures():
    with cd(env.path):
        with cd(env.project_name):
            run('./manage.py dumpdata --indent=4 articles.section uploads.thumbnailsize mailing_lists.mailinglist > common/fixtures/example_data.json')

######################################
# Utils
######################################

def use_virtualenv():
    # This can use prefix when it's available!
    return 'source %s/%s_ve/bin/activate && ' % (env.version_path, env.project_name)

