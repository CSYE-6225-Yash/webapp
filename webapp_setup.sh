#!/bin/bash

# Creating user and groupfor webapp with no login shell
sudo adduser $user --system --group
# Installing unzip package
sudo apt-get install unzip -y
# Creating directory csye6225 in opt directory
sudo mkdir -p /opt/csye6225/webapp
# Unzipping webapp.zip located at tmp in above created directory
sudo unzip /tmp/webapp.zip -d /opt/csye6225/webapp
# Changing directory to tmp
cd /tmp
# Downloading cloudwatch agent from aws
wget https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
# Installing cloudwatch agent
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
# Changing location of the cloud-watch-agentconfiguration file
sudo mv cloudwatch-agent-config.json /opt
# Creating log file for webapp
sudo mkdir -p /var/log/webapp
sudo touch /var/log/webapp/csye6225.log
# Changing ownership of that file
sudo chown -R $user:$user /var/log/webapp
sudo chmod -R 755 /var/log/webapp
# Switching to webapp directory
cd /opt/csye6225/webapp
# Installing required dependencies to run application
sudo apt-get install python3-pip -y
sudo apt-get install python3-venv -y
sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential -y
# Creating virtual environment
sudo python3 -m venv appenv
# Activating virtual environment and
# Installing all the required python packages in virtual environment
sudo bash -c "source appenv/bin/activate && pip install -r requirements.txt"
# Making created user and group owner of the webapp directory
sudo chown -R $user:$user /opt/csye6225/webapp
# Granting required permissions for webapp directory
sudo chmod -R 755 /opt/csye6225/webapp
# Creating service file for webapp so that it can run as a service
sudo bash -c "cat > /etc/systemd/system/webapp.service << EOF
[Unit]
Description=CSYE 6225 Web App
ConditionPathExists=/opt/csye6225/webapp
After=network.target

[Service]
Type=simple
User=$user
Group=$user
WorkingDirectory=/opt/csye6225/webapp
ExecStartPre=/bin/bash -c 'source appenv/bin/activate && python3 manage.py makemigrations'
ExecStartPre=/bin/bash -c 'source appenv/bin/activate && python3 manage.py migrate'
ExecStart=/bin/bash -c 'source appenv/bin/activate && python3 manage.py runserver 0.0.0.0:8000'
Restart=always
RestartSec=3
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=csye6225

[Install]
WantedBy=multi-user.target
EOF"
# Reloading background services/processes
sudo systemctl daemon-reload
# Enabling created webapp service which will run the app
sudo systemctl enable webapp.service