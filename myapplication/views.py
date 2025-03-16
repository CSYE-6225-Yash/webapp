from .models import *
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timezone
from django.db.utils import OperationalError
from django.shortcuts import redirect
import boto3
from decouple import config
import uuid

# Function for handling /healthz endpoint
def insert_record(request):
    # If request is a get request
    if request.method == "GET":
        # If request contains body or query params then return 400 Bad request
        if request.body or request.GET:
            response = HttpResponse(status=400)
            response.headers["Cache-Control"] = "no-cache"
            return response
        else:
            # Checking if database connection is active or not if not then returning 503 else returning 200
            try:
                obj = HealthCheck()
                obj.date_time = datetime.now(timezone.utc)
                obj.save()
            except OperationalError:
                response = HttpResponse(status=503)
                response.headers["Cache-Control"] = "no-cache"
                return response
            response = HttpResponse(status=200)
            response.headers["Cache-Control"] = "no-cache"
            return response
    else:
        # For every other type of request then get returning 405
        response = HttpResponse(status=405)
        response.headers["Cache-Control"] = "no-cache"
        return response

# Function for handling /v1/file/user_id endpoint
def handle_user_file(request, id):
    # If request is a get request then return user data
    if request.method == "GET":
        try:
            # Getting user data object if it exists otherwise this will raise exception and return 404
            user_obj = UserData.objects.get(user_id=id)
            response_data = {
                "file_name" : user_obj.file_name,
                "id" : user_obj.user_id,
                "url" : user_obj.url,
                "upload_date" : user_obj.upload_date
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            return redirect("not found")
    # If request is a delete and contains a valid user id then delete and return 204
    elif request.method == "DELETE":
        try:
            # Getting user id if it exists otherwise will raise exception
            user_obj = UserData.objects.get(user_id=id)
            # Creating s3 client
            s3 = boto3.client("s3")
            object_key = f"{user_obj.user_id}/{user_obj.file_name}"
            # Deleting object from s3
            s3.delete_object(Bucket=config('BUCKET_NAME'), Key=object_key)
            # Deleting database entry
            user_obj.delete()
            response = HttpResponse(status=204)
            response.headers["Cache-Control"] = "no-cache"
            return response
        except Exception as e:
            return redirect("not found")
    else:
        # For every other type of request then get returning 405
        response = HttpResponse(status=405)
        response.headers["Cache-Control"] = "no-cache"
        return response

# function for handling /v1/file endpoint
def handle_add_user_file(request):
    # If request is a post request then getting file and uploading it to the aws s3 and returning json response
    if request.method == "POST":
        try:
            # Getting file from request
            file_to_upload = request.FILES["profilePic"]
            # Creating unique user id
            user_id = uuid.uuid4()
            # Setting upload date
            upload_date = datetime.now().date()
            # Setting url
            url = f"{config('BUCKET_NAME')}/{user_id}/{file_to_upload.name}"
            # Creating s3 client
            s3 = boto3.client("s3")
            # Creating object key
            object_key = f"{user_id}/{file_to_upload.name}"
            # Uploading file to object
            s3.upload_fileobj(file_to_upload, config('BUCKET_NAME'), object_key)
            # Storing metadata in database
            user_data_obj = UserData(user_id=user_id, file_name=file_to_upload.name, url=url, upload_date=upload_date)
            user_data_obj.save()
            response_data = {
                "file_name" : file_to_upload.name,
                "id" : user_id,
                "url" : url,
                "upload_date" : upload_date
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            response = HttpResponse(status=400)
            response.headers["Cache-Control"] = "no-cache"
            return response
    # If request is a get or delete request then returning 400
    elif request.method == "GET" or request.method == "DELETE":
        response = HttpResponse(status=400)
        response.headers["Cache-Control"] = "no-cache"
        return response
    else:
        # For every other type of request then get returning 405
        response = HttpResponse(status=405)
        response.headers["Cache-Control"] = "no-cache"
        return response

# If requested other url that is not implemented then return 404 Not Found
def not_found(request):
    response = HttpResponse(status=404)
    response.headers["Cache-Control"] = "no-cache"
    return response