#Awesome Appliance Web Application#
This repo contains the code for a sample Web application that uses Apache2 and 
MySQL. It is a forms-based business app for Awesome Appliance Repair, a fictional
 appliance repair company. The app lets customers create new requests for service calls 
and lets an employee schedule and update the status of requests.

#Interacting with the application#

Here is the welcome page:

![welcome_page](images/welcome_page.png?raw=true)



If you log on as a customer, you can enter a service request in the database and 
see a list of all your requests. If you log on as an administrator, you can see all 
pending service requests. The app's landing page gives the user names and passwords 
that are required. For instance, log on as **cust1** and enter **cpw1** as the 
password. A screen appears where you can request a service call. Enter the required 
information. Here is an example.

![request_repair_cropped](images/request_repair_cropped.png?raw=true)

When you're finished, click **Submit**. You're request is acknowledged and a list 
of all your service requests is displayed.
Click **cust1:logout** at the top of the screen. The home page appears. Log in as 
an administrator by entering **ad1** as the username and **ad1pw** as the password.
 The dispatcher interface appears, which shows all service requests and their 
status. The following screenshot is an example. It shows the repair request for the 
Amana refrigerator.

![admin_page_cropped](images/admin_page_cropped.png?raw=true)

Click **logout**. The home page appears. To reset the database to its initial 
values, click **Reset Data**.

#Implementation#
The Awesome Appliance web application is written in Python and uses the Flask 
microframework. Data is stored in a MySQL database.

#Installing the application#

The following procedure has been tested on Ubuntu Server 12.04 LTS.

 1. Make sure apache2, mysql and unzip have been installed on the target host. 
You'll need to possess the root db password for MySQL.
 2. wget https://github.com/colincam/Awesome-Appliance-Repair/archive/master.zip
 3. unzip master.zip
 4. cd into Awesome-Appliance-Repair
 5. sudo mv AAR to /var/www/
 6. sudo su root
 7. run script: python AARinstall.py
 8. manually execute: apachectl graceful

#Live demo#
You can view a running version of the application at 
(http://awesome.modeled-computation.com).