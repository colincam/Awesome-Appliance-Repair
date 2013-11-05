#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen
import os, binascii

# move AAR directory to /var/www/AAR
# execute this script from your home dir

if __name__ == '__main__':
    print "testing a simple install"
#    proclog = open('./proc.log', 'w')
    
#     proc = subprocess.Popen(['apt-get', 'update', '-y'], shell=False, stdout=proclog)
#     proc.wait()
#     
#     proc = subprocess.Popen(['apt-get', 'dist-upgrade', '-y'], shell=False, stdout=proclog)
#     proc.wait()


# apt-get the stuff we need    
    proc = Popen([
        'apt-get', 'install', '-y',
        'apache2',
        'libapache2-mod-wsgi',
        'mysql-server',
        'mysql-client',
        'python-pip',
        'python-mysqldb',
        'unzip'], shell=False)
    proc.wait()

# pip install flask
    Popen(['pip', 'install', 'flask'], shell=False).wait()

# move the apache config file to sites-enabled
    Popen(['mv', './AAR-apache.conf', '/etc/apache2/sites-enabled'], shell=False)wait()
    
# start apache
    Popen(['apachectl', 'start'], shell=False).wait()

# Create AAR_config.py with secrets    
    f = open('/var/www/AAR/AAR_config.py', 'w')
    appdbpw = binascii.b2a_base64(os.urandom(6)).strip('\n')
    secretkey = binascii.b2a_base64(os.urandom(6)).strip('\n')
    
    conn_args_string = """CONNECTION_ARGS = {"host":"localhost", "user":"aarapp", "passwd":"%s", "db":"AARdb"}\n\n""" % appdbpw
    
    secret_key_string = """SECRET_KEY = "%s"\n\n """ % secretkey
    
    reset_data_string = """
    RESET_DATA = [(None, 'pending', 100), ('2013-11-01', 'completed', 101), (None, 'pending', 102), ('2013-11-02', 'completed', 103), ('2013-11-03', 'pending', 104), ('2013-11-04', 'pending', 105), (None, 'pending', 106), ('2013-11-05', 'pending', 107), (None, 'pending', 108), ('2013-11-06', 'completed', 109), (None, 'pending', 110), ('2013-11-07', 'completed', 111), (None, 'pending', 112), ('2013-11-08', 'completed', 113), (None, 'pending', 114), ('2013-11-09', 'completed', 115), (None, 'pending', 116), ('2013-11-10', 'pending', 117), (None, 'pending', 118), ('2013-11-11', 'pending', 119), (None, 'pending', 120), ('2013-11-12', 'pending', 121), (None, 'pending', 122), ('2013-11-13', 'pending', 123), (None, 'pending', 124), ('2013-11-14', 'pending', 125), (None, 'pending', 126), ('2013-11-15', 'pending', 127)]
    """
    
    f.write(conn_args_string + secret_key_string + reset_data_string)

# Create the database
    Popen("mysql -u root < make_AARdb.sql", shell=True).wait()
    
# Create DB user and permissions (it's gonna break here isn't it)
    import MySQLdb
    db = MySQLdb.connect(user='root', host='localhost', db='AARdb')
    cur = db.cursor()
    cur.execute("CREATE USER 'aarapp'@'localhost' IDENTIFIED BY %s", (appdbpw,))
    cur.execute("GRANT CREATE,INSERT,DELETE,UPDATE,SELECT on AARdb.* to aarapp@localhost")










# 
# ### now get AAR dir; from github? (reorganize dir struct first AAR w/app files, outside AAR apache config and this install.py file
# # wget https://github.com/colincam/Awesome-Appliance-Repair/archive/master.zip
# # unzip, then mv to AAR at /var/www
# 
# ### also use os.chmod(path, mode) and os.chown(path, uid, gid)
# 
# ## create AAR_config.py programmatically
# # Do this from w/in python script: generate db pw and writing it and 'secret key' to AAR_config.py
# 
# # then do
# # mysql -u root < make_AARdb.sql
# 
# # for pw and secret string use 
# # binascii.b2a_base64(os.urandom(6)).strip('\n')
# # then using mysqldb do
# # CREATE USER 'aarapp'@'localhost' IDENTIFIED BY 'OTC8eLTXr2mW&cjY';
# # GRANT CREATE,INSERT,DELETE,UPDATE,SELECT on AARdb.* to aarapp@localhost;
# 
# 
# 
# #### AAAArgh!! DO NOT TRY TO INSTALL MySQLdb WITH PIP!!! USE THIS INSTEAD:
# ### sudo apt-get install python-mysqldb
# ### TODO
# # Create database thus:
# # mysql -u root < make_AARdb.sql
# # create the aarapp user and pw for the webapp to use, and grant permissions
# # (can I write this into the .sql file?
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # install pip with easy_install
# # update pip
# # install MySQLdb python module
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # get the AAR repo from github: no need to do this
# # 
# # os.chdir('/var/www')
# # use Popen for:
# # wget https://github.com/colincam/Awesome-Appliance-Repair/archive/master.zip
# # 
# # unzip into /var/www/AAR
# # 
# # Then chown and chmod as needed
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # edit apache config file at /etc/apache2/sites-enabled/000-default
# # adding the mod_wsgi stuff
# # apachectl restart
# # 
# # and then it 'just works', HA.

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    