# System preparation
package {
    "build-essential": ensure => "latest";
    "locales": ensure => "latest";
}

file {
    "/etc/locale.gen":
        content => template("files/etc/locale.gen"),
        owner => "root",
        group => "root",
        mode => 644,
        require => Package[locales];
}
file {
    "/etc/default/locale":
        content => template("files/etc/default/locale"),
        owner => "root",
        group => "root",
        mode => 644,
        require => Package[locales];
}

exec { "/usr/sbin/locale-gen":
    subscribe => File["/etc/locale.gen"],
    refreshonly => true,
    require => [Package[locales], File["/etc/locale.gen"]],
}

file {
    "/etc/bash.bashrc":
        content => template("files/etc/bash.bashrc"),
        owner => "root",
        group => "root",
        mode => 644;
}

# Packages for Boar site
package {
    "supervisor": ensure => "latest";
    "nginx": ensure => "latest";
    "redis-server": 
        provider => dpkg,
        source => "packages/redis-server_2.2.10-1_i386.deb";
    "postgresql-8.4": ensure => "latest";
    "python-virtualenv": ensure => "latest";
    "git-core": ensure => "latest";
    "python-cairo": ensure => "latest";
    "python-cjson": ensure => "latest";
    "python-imaging": ensure => "latest";
    "python-psycopg2": ensure => "latest";
    "python-setuptools": ensure => "latest";
    "python-dev": ensure => "latest";
    "csstidy": ensure => "latest";
    "imagemagick": ensure => "latest";
}

# GeoDjango
package {
    "binutils": ensure => "latest";
    "postgresql-8.4-postgis": ensure => "latest";
}

# Solr --------------------------------------------------------------
package {
    "jetty": ensure => "latest";
    "libjetty-extra-java": ensure => "latest";
    "glassfish-mail": ensure => "latest";
    "libcommons-codec-java": ensure => "latest";
    "libcommons-csv-java": ensure => "latest";
    "libcommons-fileupload-java": ensure => "latest";
    "libcommons-httpclient-java": ensure => "latest";
    "libcommons-io-java": ensure => "latest";
    "libjaxp1.3-java": ensure => "latest";
    "libjetty-java": ensure => "latest";
    "liblucene2-java": ensure => "latest";
    "libservlet2.5-java": ensure => "latest"; 
    "libslf4j-java": ensure => "latest";
    "libxml-commons-external-java": ensure => "latest";
    "openjdk-6-jre-headless": ensure => "latest";
    "openjdk-6-jdk": ensure => "latest";
    "solr-common": 
        provider => dpkg,
        source => "packages/solr-common_1.4.1+dfsg1-2_all.deb",
        require => [
            Package["glassfish-mail"],
            Package["libcommons-codec-java"],
            Package["libcommons-csv-java"],
            Package["libcommons-fileupload-java"],
            Package["libcommons-httpclient-java"],
            Package["libcommons-io-java"],
            Package["libjaxp1.3-java"],
            Package["libjetty-java"],
            Package["liblucene2-java"],
            Package["libservlet2.5-java"],
            Package["libslf4j-java"],
            Package["libxml-commons-external-java"],
            Package["openjdk-6-jre-headless"]
        ];
    "solr-jetty":
        provider => dpkg,
        source => "packages/solr-jetty_1.4.1+dfsg1-2_all.deb",
        require => [
            Package["solr-common"],
            Package["jetty"],
            Package["libjetty-extra-java"],
            Package["openjdk-6-jdk"]
        ];
}

file {
    "/etc/default/jetty":
        content => template("files/etc/default/jetty"),
        require => Package["jetty"];
}

service { "jetty":
    enable => true,
    ensure => running,
    require => Package["jetty"],
    subscribe => File["/etc/default/jetty"]
}
# End of Solr --------------------------------------------------------

file { "/var/www":
    ensure => directory,
    owner => www-data,
    group => www-data
}

file { "/var/www/theboar.org":
    ensure => directory,
    owner => www-data,
    group => www-data,
    require => File["/var/www"]
}


file { "/var/www/theboar.org/media":
    ensure => directory,
    owner => www-data,
    group => www-data,
    require => File["/var/www/theboar.org"]
}

file { "/var/www/theboar.org/celery":
    ensure => directory,
    owner => www-data,
    group => www-data,
    require => File["/var/www/theboar.org"]
}
file {
    "/etc/supervisor/supervisord.conf":
        content => template("files/etc/supervisor/supervisord.conf"),
        require => Package[supervisor];
}
file {
    "/etc/supervisor/conf.d/gunicorn.conf":
        content => template("files/etc/supervisor/conf.d/gunicorn.conf"),
        require => Package[supervisor];
}
file {
    "/etc/supervisor/conf.d/celeryd.conf":
        content => template("files/etc/supervisor/conf.d/celeryd.conf"),
        require => Package[supervisor];
}
file {
    "/etc/supervisor/conf.d/celerybeat.conf":
        content => template("files/etc/supervisor/conf.d/celerybeat.conf"),
        require => Package[supervisor];
}


service { "supervisor":
    enable => true,
    ensure => running,
    require => Package["supervisor", "nginx"], 
    subscribe => [
        Package["supervisor"],
        File["/etc/supervisor/conf.d/gunicorn.conf"],
        File["/etc/supervisor/conf.d/celeryd.conf"],
        File["/etc/supervisor/conf.d/celerybeat.conf"]
    ]
}

file {
    "/etc/nginx/sites-available/default":
        content => template("files/etc/nginx/sites-available/default"),
        require => Package[nginx];
}

service { "nginx":
    enable => true,
    ensure => running,
    require => Package["nginx"], 
    subscribe => [
        Package["nginx"],
        File["/etc/nginx/sites-available/default"]
    ]
}



