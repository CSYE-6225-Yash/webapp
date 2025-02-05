#!/bin/bash

# 1.Update the package list for upgrade
sudo apt-get update
# 2. Upgrade the packages with yes flag
sudo apt-get upgrade -y
# 3. Installing Mysql server
sudo apt-get install mysql-server -y
# running mysql default security script which deletes test databases and blocks all remote connection by default
sudo mysql_secure_installation
# accessing mysql as a root user
# note that here no password is required because it uses auth_socket
# auth_socket matches linux system user with the database user and grants permission
# 4. Creating database if it doesnt exist
dbname="webdb"
dbexist=false
sudo mysql -e "create database $dbname;" || dbexist=true
if $dbexist; then
    echo "Database already exists so skiping further database steps"
else
    # taking database password from user
    read -sp "Enter database password : " dbpass
    # creating a new user in mysql which has permission of only this database
    sudo mysql -e "create user 'webapp'@'localhost' identified by '$dbpass';"
    # grantint all permission to that user on database
    sudo mysql -e "grant all privileges on $dbname.* to 'webapp'@'localhost';"
fi
# 5. Create linux group for application
sudo groupadd webapp
# 6. Creating user for application and adding it to webapp group
sudo useradd -g webapp webapp
# 7. Unzip the application in /opt/csye6225
# installing unzip 
sudo apt-get install unzip -y
# making csye6225 directory in opt if it doesn't exist and creating venv and application user
# otherwise changing directory and running application
if [ ! -d "/opt/csye6225/webapp" ]; then
    sudo mkdir -p /opt/csye6225
    sudo unzip webapp.zip -d /opt/csye6225
    # taking django secret key from user which is required in .env file
    read -sp "Enter django secret key : " secretkey
    # changing directory to webapp
    cd /opt/csye6225/webapp
    # installing python pip (package installer)
    sudo apt-get install python3-pip -y
    # installing python venv (for creating virtual environments)
    sudo apt-get install python3-venv -y
    # installing other packages which are required
    sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential -y
    # creating virtual environment
    sudo python3 -m venv appenv
    # activating that virtual environment
    source appenv/bin/activate
    # installing all requirements from requirements.txt file
    pip install -r requirements.txt
    # 8. Update the permissions of the folder
    # make the application user a owner and webapp group which we created earlier a group that own this folder
    sudo chown -R webapp:webapp /opt/csye6225/webapp
    # provide appropriate permissions to the folder
    sudo chmod -R 755 /opt/csye6225/webapp
    # create .env file and put content in it
    if ! $dbexist; then
        sudo runuser webapp -c "cat > /opt/csye6225/webapp/.env << EOF
        DEBUG=True
        SECRET_KEY=$secretkey
        DATABASE_NAME=$dbname
        DATABASE_USER=webapp
        DATABASE_PASSWORD=$dbpass
        DATABASE_Host=localhost
        DATABASE_PORT=3306
        EOF"
    fi
    else
    # changing directory to webapp
    cd /opt/csye6225/webapp
fi
# running application through application user that was created
sudo -u webapp bash -c "source appenv/bin/activate && python3 manage.py makemigrations"
sudo -u webapp bash -c "source appenv/bin/activate && python3 manage.py migrate"
sudo -u webapp bash -c "source appenv/bin/activate && python3 manage.py runserver 0.0.0.0:8000"