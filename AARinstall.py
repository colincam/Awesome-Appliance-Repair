#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen
import os, binascii

# This assumes that apt-get update, and apt-get dist-upgrade, AND
# apt-get install apache2 AND unzip have been done. The script below
# includes Apache, but apt-get does the right thing and simply
# notes that the existing version is up to date.
# 
# 1. wget https://github.com/colincam/Awesome-Appliance-Repair/archive/master.zip
# 2. unzip master.zip
# 3. cd into Awesome-Appliance-Repair
# 4. sudo mv AAR to /var/www/
# 5. sudo su root
# 6. run script: python AARinstall.py
# 7. each time a password is asked for mysql root user, just hit return
#       would this work to get rid of the interactive pw prompts?
#         export DEBIAN_FRONTEND=noninteractive
#         apt-get -q -y install mysql-server
#
# To my astonishment, this worked on almost the first try.
# It shouldn't have worked at all: missing is a step to chown and chmod the application files.

if __name__ == '__main__':

# apt-get the stuff we need    
    proc = Popen([
        'apt-get', 'install', '-y',
        'apache2',
        'libapache2-mod-wsgi',
        'mysql-server',
        'mysql-client',
        'python-pip',
        'python-mysqldb'], shell=False)
    proc.wait()

# pip install flask
    Popen(['pip', 'install', 'flask'], shell=False).wait()

# move the apache config file to sites-enabled
    Popen(['mv', './AAR-apache.conf', '/etc/apache2/sites-enabled'], shell=False).wait()
    
# Create AAR_config.py with secrets    
    f = open('/var/www/AAR/AAR_config.py', 'w')
    appdbpw = binascii.b2a_base64(os.urandom(6)).strip('\n')
    secretkey = binascii.b2a_base64(os.urandom(6)).strip('\n')
    
    conn_args_string = """CONNECTION_ARGS = {"host":"localhost", "user":"aarapp", "passwd":"%s", "db":"AARdb"}\n\n""" % appdbpw
    
    secret_key_string = """SECRET_KEY = "%s"\n\n""" % secretkey
    
    reset_data_string = """RESET_DATA = [(None, 'pending', 100), ('2013-11-01', 'completed', 101), (None, 'pending', 102), ('2013-11-02', 'completed', 103), ('2013-11-03', 'pending', 104), ('2013-11-04', 'pending', 105), (None, 'pending', 106), ('2013-11-05', 'pending', 107), (None, 'pending', 108), ('2013-11-06', 'completed', 109), (None, 'pending', 110), ('2013-11-07', 'completed', 111), (None, 'pending', 112), ('2013-11-08', 'completed', 113), (None, 'pending', 114), ('2013-11-09', 'completed', 115), (None, 'pending', 116), ('2013-11-10', 'pending', 117), (None, 'pending', 118), ('2013-11-11', 'pending', 119), (None, 'pending', 120), ('2013-11-12', 'pending', 121), (None, 'pending', 122), ('2013-11-13', 'pending', 123), (None, 'pending', 124), ('2013-11-14', 'pending', 125), (None, 'pending', 126), ('2013-11-15', 'pending', 127)]
    """
    
    f.write(conn_args_string + secret_key_string + reset_data_string)
    f.close()
    
# Create the database
    Popen("mysql -u root < make_AARdb.sql", shell=True).wait()
    
# Create DB user and permissions
    import MySQLdb
    db = MySQLdb.connect(user='root', host='localhost', db='AARdb')
    cur = db.cursor()
    cur.execute("CREATE USER 'aarapp'@'localhost' IDENTIFIED BY %s", (appdbpw,))
    cur.execute("GRANT CREATE,INSERT,DELETE,UPDATE,SELECT on AARdb.* to aarapp@localhost")

# restart apache
    Popen(['apachectl', 'restart'], shell=False).wait()
