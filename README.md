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