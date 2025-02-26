#!/bin/bash

# Removing git which comes by default in ubuntu
sudo apt-get remove --purge git -y
# Removing unnecessary packages
sudo apt-get autoremove -y
# Updating pacakge list
sudo apt-get update
# Installing updated packages from updated pacakge list
sudo apt-get upgrade -y