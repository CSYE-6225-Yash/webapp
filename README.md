# Building application locally

First you need to clone this repositoty to your pc.

After you have cloned it you can create a virtual environment or run it directly but make sure you have python installed on your system.

To create virtual env you need to type command -

`python -m venv name_of_env`

Then activate virtual environment (if you have created one) using following commands -

On Windows - `venv\Scripts\activate`

On Linux/Mac - `source venv/bin/activate`

Then install required python packages to run the app using requirements.txt file -

`pip install -r requirements.txt`


You also need to create `.env` file in root directory because some credentials and other variables that are required are stored in it.

You also need to install `MYSQL` server because I have used mysql database.

After you are done with installing mysql then you need to create database using sql command in mysql and supply that database all the credentials in the .env file.

After that you just need to run commands -

`python manage.py makemigrations`

`python manage.py migrate`

# Deploying app locally

To run a development server you need to run command -

`python manage.py runserver`

After running this command your server will run on localhost:8000 port by default.

# Running test cases

To run test cases you need to run command -

`python manage.py test`

# Running automated setup on linux

Instead of doing all the setup of application manually you can do this all setup just in one command by running `automated_setup.sh` on ubuntu but it requires `webapp.zip` file in same location as of automated_setup file so make sure to do that.

You can run .sh (shell scripts) in linux as -

`./file_name.sh` in this case `./automated_setup.sh`

also make sure to make sure that the shell script file (.sh file) has appropriate permission to execute.

# Configure aws-cli using following steps -

For creating aws-cli profile use following command -

`aws configure --profile profile_name`

For using that profile you need to setup temparary environment variables in your system do this with following command -

For windows -

`set AWS_PROFILE=profile_name`

For linux/mac -

`export AWS_PROFILE=profile_name`

# Set up gcloud-cli using following steps -

For configuring gcloud-cli profile use following command -

`gcloud config configurations create config_name`

For activating created configuration use -

`gcloud config configurations activate config_name`

For authenticating using cli create a service account in IAM amd then generate json file and then use following command -

`auth login --cred-file=key_file`

For packer to use gcp key you need to set environment variable containing that key file location -

For windows -

`set GOOGLE_APPLICATION_CREDENTIALS=key_file`

For linux/mac -

`export GOOGLE_APPLICATION_CREDENTIALS=key_file`

# Packer basic commands to get started with custom machine image building -

`packer init .` - this command initializes packer and installs required plugins.

- Note that in above command `.` refers to the current directory that contains packer template you can specify any other path or file if you want

`packer fmt .` - this command correctly formats the packer files with correct indentation and spacing.

`packer validate -var-file=var.pkrvars.hcl .` - this command validates the packer files and returns error if there is any syntax error. -var-file here is optional if you have set default variable values to "" then you might kept a variable file and need to pass that file for associating variables.

`packer build -var-file=var.pkrvars.hcl .` - this command is used to start building the custom image. 

- Note that built custom image does not contain local database and so database configuration parameters need to be uploaded with the user data script. 