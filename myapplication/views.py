from .models import *
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timezone
from django.db.utils import OperationalError
from django.shortcuts import redirect
import boto3
from decouple import config
import uuid
import logging
import time
from statsd.defaults.django import statsd

# Creating logger instance
logger = logging.getLogger("webapp")

# Creating default logger functions that will be called to log into a file and returns current time
def request_received_log(request, endpoint):
    # Counting_api_calls
    statsd.incr(f'{endpoint}_{request.method}')
    # Adding log entry that request is received
    logger.info(f"{endpoint} endpoint Received {request.method} request from {request.META.get('REMOTE_ADDR')}")
    return time.time()

def request_response_log(request, response, endpoint, request_start_time):
    # Adding log entry for server response
    if response.status_code < 500:
        logger.info(f"Server Responded {response.status_code} to {request.method} request received from {request.META.get('REMOTE_ADDR')} via {endpoint} endpoint")
    else:
        logger.error(f"Server Responded {response.status_code} to {request.method} request received from {request.META.get('REMOTE_ADDR')} via {endpoint} endpoint", exc_info=True)
    # Adding metric of time request took
    statsd.timing(f"{endpoint}_{request.method}_time", int((time.time() - request_start_time) * 1000))

# Function for handling /healthz endpoint
def insert_record(request):
    # Adding log entry
    request_start_time = request_received_log(request, "/healthz")
    # If request is a get request
    if request.method == "GET":
        # If request contains body or query params then return 400 Bad request
        if request.body or request.GET:
            response = HttpResponse(status=400)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/healthz", request_start_time)
            return response
        else:
            # Checking if database connection is active or not if not then returning 503 else returning 200
            try:
                # Adding timing data in metrics
                start_db_query = time.time()
                obj = HealthCheck()
                obj.date_time = datetime.now(timezone.utc)
                obj.save()
                statsd.timing("database_add_query", int((time.time() - start_db_query) * 1000))
            except OperationalError:
                response = HttpResponse(status=503)
                response.headers["Cache-Control"] = "no-cache"
                # Adding log entry
                request_response_log(request, response, "/healthz", request_start_time)
                return response
            response = HttpResponse(status=200)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/healthz", request_start_time)
            return response
    else:
        # For every other type of request then get returning 405
        response = HttpResponse(status=405)
        response.headers["Cache-Control"] = "no-cache"
        # Adding log entry
        request_response_log(request, response, "/healthz", request_start_time)
        return response

# Function for handling /v1/file/user_id endpoint
def handle_user_file(request, id):
    # Adding log entry
    request_start_time = request_received_log(request, "/v1/file/user_id")
    # If request is a get request then return user data
    if request.method == "GET":
        try:
            # Getting user data object if it exists otherwise this will raise exception and return 404
            # Adding timing data in metrics
            start_db_query = time.time()
            user_obj = UserData.objects.get(user_id=id)
            statsd.timing("database_get_query", int((time.time() - start_db_query) * 1000))
            response_data = {
                "file_name" : user_obj.file_name,
                "id" : user_obj.user_id,
                "url" : user_obj.url,
                "upload_date" : user_obj.upload_date
            }
            response = JsonResponse(response_data, status=200)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/v1/file/user_id", request_start_time)
            return response
        except Exception as e:
            response = HttpResponse(status=404)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/v1/file/user_id", request_start_time)
            return response
    # If request is a delete and contains a valid user id then delete and return 204
    elif request.method == "DELETE":
        try:
            # Getting user id if it exists otherwise will raise exception
            # Adding timing data in metrics
            start_db_query = time.time()
            user_obj = UserData.objects.get(user_id=id)
            statsd.timing("database_get_query", int((time.time() - start_db_query) * 1000))
            # Creating s3 client
            # Adding timing data in metrics
            start_s3_call = time.time()
            s3 = boto3.client("s3")
            object_key = f"{user_obj.user_id}/{user_obj.file_name}"
            # Deleting object from s3
            s3.delete_object(Bucket=config('BUCKET_NAME'), Key=object_key)
            statsd.timing("s3_api_delete", int((time.time() - start_s3_call) * 1000))
            start_db_query = time.time()
            # Deleting database entry
            user_obj.delete()
            statsd.timing("database_delete_query", int((time.time() - start_db_query) * 1000))
            response = HttpResponse(status=204)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/v1/file/user_id", request_start_time)
            return response
        except Exception as e:
            response = HttpResponse(status=404)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/v1/file/user_id", request_start_time)
            return response
    else:
        # For every other type of request then get returning 405
        response = HttpResponse(status=405)
        response.headers["Cache-Control"] = "no-cache"
        # Adding log entry
        request_response_log(request, response, "/v1/file/user_id", request_start_time)
        return response

# function for handling /v1/file endpoint
def handle_add_user_file(request):
    # Adding log entry
    request_start_time = request_received_log(request, "/v1/file")
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
            start_s3_call = time.time()
            s3 = boto3.client("s3")
            # Creating object key
            object_key = f"{user_id}/{file_to_upload.name}"
            # Uploading file to object
            s3.upload_fileobj(file_to_upload, config('BUCKET_NAME'), object_key)
            statsd.timing("s3_api_file_upload", int((time.time() - start_s3_call) * 1000))
            start_s3_call = time.time()
            # Getting object metadata
            metadata = s3.head_object(Bucket=f"{config('BUCKET_NAME')}", Key=object_key)
            statsd.timing("s3_api_get_obj_metadata", int((time.time() - start_s3_call) * 1000))
            try:
                metadata["LastModified"] = metadata["LastModified"].isoformat()
                metadata["Expires"] = metadata["Expires"].isoformat()
                metadata["ObjectLockRetainUntilDate"] = metadata["ObjectLockRetainUntilDate"].isoformat()
            except:
                pass
            # Storing metadata in database
            start_db_query = time.time()
            user_data_obj = UserData(user_id=user_id, file_name=file_to_upload.name, url=url, upload_date=upload_date, obj_metadata=metadata)
            user_data_obj.save()
            statsd.timing("database_add_query", int((time.time() - start_db_query) * 1000))
            response_data = {
                "file_name" : file_to_upload.name,
                "id" : user_id,
                "url" : url,
                "upload_date" : upload_date
            }
            response = JsonResponse(response_data, status=201)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/v1/file", request_start_time)
            return response
        except Exception as e:
            response = HttpResponse(status=400)
            response.headers["Cache-Control"] = "no-cache"
            # Adding log entry
            request_response_log(request, response, "/v1/file", request_start_time)
            return response
    # If request is a get or delete request then returning 400
    elif request.method == "GET" or request.method == "DELETE":
        response = HttpResponse(status=400)
        response.headers["Cache-Control"] = "no-cache"
        # Adding log entry
        request_response_log(request, response, "/v1/file", request_start_time)
        return response
    else:
        # For every other type of request then get returning 405
        response = HttpResponse(status=405)
        response.headers["Cache-Control"] = "no-cache"
        # Adding log entry
        request_response_log(request, response, "/v1/file", request_start_time)
        return response

# If requested other url that is not implemented then return 404 Not Found
def not_found(request):
    # Adding log entry
    request_start_time = request_received_log(request, "Unimplemented")
    response = HttpResponse(status=404)
    response.headers["Cache-Control"] = "no-cache"
    # Adding log entry
    request_response_log(request, response, "Unimplemented", request_start_time)
    return response