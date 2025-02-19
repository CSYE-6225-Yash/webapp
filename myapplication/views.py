from .models import *
from django.http import HttpResponse
from datetime import datetime, timezone
from django.db.utils import OperationalError

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

# If requested other url than healthz then return 404 Not Found
def not_found(request):
    response = HttpResponse(status=404)
    #response.headers["Cache-Control"] = "no-cache"
    return response