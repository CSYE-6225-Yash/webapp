#!/bin/bash

# 1.Update the package list for upgrade
sudo apt-get update
# 2. Upgrade the packages with yes flag
sudo apt-get upgrade -y
# 3. Installing Mysql server
sudo apt-get install mysql-server
# running mysql default security script which deletes test databases and blocks all remote connection by default
sudo mysql_secure_installation
# accessing mysql as a root user
# note that here no password is required because it uses auth_socket
# auth_socket matches linux system user with the database user and grants permission
# 4. Creating database
sudo mysql -e "create database webdb;"
# creating a new user in mysql which has permission of only this database
sudo mysql -e "create user 'webapp'@'localhost' identified with auth_socket;"
# grantint all permission to that user on database
sudo mysql -e "grant all privileges on webdb.* to 'webapp'@'localhost';"
# 5. Create linux group for application
sudo groupadd webapp
# 6. Creating user for application and adding it to webapp group
sudo useradd -g webapp webapp
# 7. Unzip the application in /opt/csye6225
# installing unzip 
sudo apt-get install unzip
# making csye6225 directory in opt if it doesn't exist
sudo mkdir -p /opt/csye6225
sudo unzip webapp.zip -d /opt/csye6225
# 8. Update the permissions of the folder
# make the application user a owner and webapp group which we created earlier a group that own this folder
sudo chown -R webapp:webapp /opt/csye6225/webapp
# provide appropriate permissions to the folder
sudo chmod -R 755 /opt/csye6225/webapp