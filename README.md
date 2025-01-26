# Requirements

`pip install django`

`pip install decouple`

Mysql server

# Building application locally

In django first we need to create a project with command -

`django-admin startproject project_name directory_name`

Then we need to create app with command -

`django-admin startapp app_name`

You also need to create `.env` file in root directory because some credentials and other variables that are required are stored in it.

# Deploying app locally

To run a development server you need to run command -

`python manage.py runserver`

After running this command your server will run on localhost:8000 port by default.