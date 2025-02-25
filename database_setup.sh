#!/bin/bash

# Installing mysql server
sudo apt-get install mysql-server -y
# Creating database
sudo mysql -e "create database $dbname;" || true
# Creating database user and setting his password
sudo mysql -e "create user '$user'@'localhost' identified by '$dbpass';"
# Granting database permissions to crated user
sudo mysql -e "grant all privileges on $dbname.* to '$user'@'localhost';"
sudo mysql -e "grant all privileges on test_$dbname.* to '$user'@'localhost';"