#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen
import os, binascii
import sys
# This assumes that apt-get update, and apt-get dist-upgrade, AND
# apt-get install apache2 AND unzip have been done. The script below
# includes Apache, but apt-get does the right thing and simply
# notes that the existing version is up to date.

# 1. wget https://github.com/colincam/Awesome-Appliance-Repair/archive/master.zip
# 2. unzip master.zip
# 3. cd into Awesome-Appliance-Repair
# 4. sudo mv AAR to /var/www/
# 5. sudo su root
# 6. run script: python AARinstall.py
# 7. each time a password is asked for mysql root user, just hit return
# To my astonishment, this worked on almost the first try.
# It shouldn't have worked at all: missing is a step to chown and chmod the application files.

## Also NB: to save a lot of pain for the installer (me) include openssh-server in the apt-get list below. That's how you can ssh into the VM (bridged networking, autodetect) and thus get scrollback, copy/paste, drag/drop

## If this version isn't satisfactory, this is the commit we should roll back to: https://github.com/colincam/Awesome-Appliance-Repair/commit/5056fa5899aeed65f85bf4f05c18b7de491a4a49

if __name__ == '__main__':
    dbpswd = sys.argv[1]

# change mode and ownership  of the files in AAR    
    Popen(['chown', '-R', 'www-data:www-data', '/var/www/AAR'], shell=False).wait()
    Popen(['chmod', '-R', '644', '/var/www/AAR'], shell=False).wait()

# apt-get the stuff we need    
    proc = Popen([
        'apt-get', 'install', '-y',
        'libapache2-mod-wsgi',
        'python-pip',
        'python-mysqldb'], shell=False)
    proc.wait()

# pip install flask
    Popen(['pip', 'install', 'flask'], shell=False).wait()

# Generate the apache config file in sites-enabled
    Popen(['apachectl', 'stop'], shell=False).wait()
    Popen(['rm', '/etc/apache2/sites-enabled/*'], shell=False).wait()
    
    f = open('/etc/apache2/sites-enabled/AAR-apache.conf', 'w')
    f.write("""
    <VirtualHost *:80>
      ServerName /
      WSGIDaemonProcess /AAR user=www-data group=www-data threads=5
      WSGIProcessGroup /AAR
      WSGIScriptAlias / /var/www/AAR/awesomeapp.wsgi

      <Directory /var/www/AAR>
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
      </Directory>

      ServerAdmin ops@example.com
    </VirtualHost>
    """)
    f.close()
    
# Generate AAR_config.py with secrets    
    f = open('/var/www/AAR/AAR_config.py', 'w')
    appdbpw = binascii.b2a_base64(os.urandom(6)).strip('\n')
    secretkey = binascii.b2a_base64(os.urandom(6)).strip('\n')
    
    conn_args_string = """CONNECTION_ARGS = {"host":"localhost", "user":"aarapp", "passwd":"%s", "db":"AARdb"}\n\n""" % appdbpw
    
    secret_key_string = """SECRET_KEY = "%s"\n\n""" % secretkey
    
    database_values_string = """DB_VALUES = [(3,'Maytag','Washer', None, 'pending', "outflow hoses leak"),(4,'GE','Refrigerator', '2013-11-01', 'completed', "Ices up; won't defrost"), (5,'Alessi','Teapot', None, 'pending', "explodes"), (6,'Amana','Range', '2013-11-02', 'completed', "oven heats unevenly"), (7,'Whirlpool','Refrigerator', '2013-11-03', 'pending', "Makes a rattling noise"), (8,'GE','Microwave', '2013-11-04', 'pending', "Sparks and smokes when I put forks in it"), (9,'Maytag','Drier', None, 'pending', "Never heats up"), (10,'Amana','Refrigerator', '2013-11-05', 'pending', "Temperature too low, can't adjust."), (11,'Samsung','Washer', None, 'pending', "Doesn't get my bear suit white"), (12,'Frigidaire','Refrigerator', '2013-11-06', 'completed', "Has a bad smell I can't get rid of."), (13,'In-Sink-Erator','Dispose-all', None, 'pending', "blades broken"), (14,'KitchenAid','Mixer', '2013-11-07', 'completed', "Blows my fuses"), (15,'Moulinex','Juicer', None, 'pending', "Won't start"), (16,'Viking','Range', '2013-11-08', 'completed', "Gas leak"), (17,'Aga','Range', None, 'pending', "burner cover is cracked"), (18,'Jennaire','Cooktop', '2013-11-09', 'completed', "Glass cracked"), (19,'Wolfe','Stove', None, 'pending', "Burners are uneven"), (20,'LG','Dehumidifier', '2013-11-10', 'pending', "Ices up when external temp is around freezing"), (21,'DeLonghi','Oil Space Heater', None, 'pending', "Smells bad"), (22,'Kenmore','Refrigerator', '2013-11-11', 'pending', "excessive vibration"), (23,'Maytag','Washer/Drier', None, 'pending', "outflow hoses leak"), (24,'GE','Refrigerator', '2013-11-12', 'pending', "Refrigerator light is defective"), (25,'Kenmore','Washer', None, 'pending', "Unbalanced spin cycle"), (26,'Cookmore','Outdoor Grill', '2013-11-13', 'pending', "Smoker box is stuck"), (27,'Kenmore','Water heater', None, 'pending', "Can't adjust temperature"), (28,'Sanyo','Minifridge', '2013-11-14', 'pending', "Makes a lot of noise"), (29,'Bosch','Dishwasher', None, 'pending', "leaves spots on my glasses"), (30,'Whirlpool','Trash Compactor', '2013-11-15', 'pending', "leaking hydraulic fluid")]
    """
    
    f.write(conn_args_string + secret_key_string + database_values_string)
    f.close()

# Create DB, user, and permissions
    import MySQLdb
    db = MySQLdb.connect(host='localhost', user='root', passwd=dbpswd)
    sql_script = open('make_AARdb.sql', 'r').read()
    
    cur = db.cursor()
    cur.execute(sql_script)
    cur.close()
        
    cur = db.cursor()
    cur.execute('use AARdb')
    cur.execute("CREATE USER 'aarapp'@'localhost' IDENTIFIED BY %s", (appdbpw,))
    cur.execute("GRANT CREATE,INSERT,DELETE,UPDATE,SELECT on AARdb.* to aarapp@localhost")
    cur.close()
    db.close()
    
    
# restart apache
    Popen(['apachectl', 'start'], shell=False).wait()

## TODO? chown and chmod of app files?