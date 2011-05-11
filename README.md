Boar website
============

Requirements
------------

 - Debian Lenny or Ubuntu
 - Python 2.5 (probably)
 - PostgreSQL 8.3

Setting up a development environment
------------------------------------

All these sequences of commands expect you to be in the same directory as this 
readme.

Fabric is needed to complete the rest of the installation:
    
    $ sudo easy_install pip
    $ sudo pip install fabric

To create a development environment in Debian, run this:

    $ fab localhost setup_dev

If ``fabfile.py`` or ``requirements.txt`` gets updated in the future, you may 
need to delete the ``boar_ve/`` directory and rerun these commands.

### Installing the database

Create a PostGIS template database:

    $ sudo su - postgres
    $ createdb -E UTF8 template_postgis
    $ createlang -d template_postgis plpgsql
    $ psql -d template_postgis -f /usr/share/postgresql-8.3-postgis/lwpostgis.sql
    $ psql -d template_postgis -f /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql

Open a shell in the template:

    $ psql -d template_postgis

And execute these SQL statements:

    GRANT ALL ON geometry_columns TO PUBLIC;
    GRANT ALL ON spatial_ref_sys TO PUBLIC;

Create a database, replacing ``username`` with your system user:

    $ sudo su postgres
    $ createdb -T template_postgis -O username boar

Run these commands to set up your database and create the superuser:

    $ cd boar/
    $ ./manage.py syncdb
    $ ./manage.py migrate

You may need to rerun these commands if there are future database changes.

Initially, you'll need a bit of data to get you started:

    $ cd boar/
    $ ./manage.py loaddata example_data


### Installing Solr

Download a recent tarball from:

http://www.apache.org/dyn/closer.cgi/lucene/solr/

Extract it and set up the configurations::

    $ tar -xzf apache-solr-1.4.0.tgz
    $ cd apache-solr-1.4.0/example/
    $ rm -rf solr
    $ ln -s `pwd`/../../solr solr

To run the Solr development server, you will need to change into 
``apache-solr-1.4.0/example/`` and run:

    $ java -jar start.jar

If you need to rebuild your Solr index, run:

    $ cd boar/
    $ ./manage.py rebuild_index


### Running the development server

With the Solr server also running:

    $ cd boar/
    $ ./manage.py runserver

