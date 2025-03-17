from django.test import TestCase
from unittest.mock import patch
from django.db.utils import OperationalError
from django.core.files.uploadedfile import SimpleUploadedFile
from decouple import config
from datetime import datetime
import json
from myapplication.models import *

# Testcases for healthz endpoint 
class AppHealthCheckTestCase(TestCase):
    # Testcase for get request without payload
    def test_get(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for get request with payload (query parameters)
    def test_get_query_params(self):
        response = self.client.get("/healthz", query_params={"name":"abc"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for get request with payload (body)
    def test_get_body(self):
        response = self.client.get("/healthz", {"name":"abc"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for post request
    def test_post(self):
        response = self.client.post("/healthz")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for put request
    def test_put(self):
        response = self.client.put("/healthz")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for delete request
    def test_delete(self):
        response = self.client.delete("/healthz")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for head request
    def test_head(self):
        response = self.client.head("/healthz")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for options request
    def test_options(self):
        response = self.client.options("/healthz")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)

    # Testcase for options request
    def test_options(self):
        response = self.client.options("/healthz")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for patch request
    def test_patch(self):
        response = self.client.patch("/healthz")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for get request but with closed database connection
    # creating a mock object for database cursor
    @patch("django.db.backends.base.base.BaseDatabaseWrapper.cursor")
    def test_get_closed_database_connection(self, mock_obj):
        # returning operation error if database instance is called
        mock_obj.side_effect = OperationalError("Connection timed out")
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 503)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for any other endpoint requested other than defined ones
    def test_undefined_endpoint(self):
        response = self.client.get("/abc")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for get request for /v1/file endpoint
    def test_get_file_without_user_id(self):
        response = self.client.get("/v1/file")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for delete request for /v1/file endpoint
    def test_delete_file_without_user_id(self):
        response = self.client.delete("/v1/file")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for head request for /v1/file endpoint
    def test_head_file_without_user_id(self):
        response = self.client.head("/v1/file")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for options request for /v1/file endpoint
    def test_options_file_without_user_id(self):
        response = self.client.options("/v1/file")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for patch request for /v1/file endpoint
    def test_patch_file_without_user_id(self):
        response = self.client.patch("/v1/file")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for put request for /v1/file endpoint
    def test_put_file_without_user_id(self):
        response = self.client.put("/v1/file")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for post request for /v1/file endpoint
    def test_post_file_without_user_id_and_no_file_supplied(self):
        response = self.client.post("/v1/file")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for post request for /v1/file endpoint
    def test_post_file_without_user_id_and_wrong_file_name(self):
        # Creating dummy file to upload
        file_data = b"abcdef"
        dummy_file = SimpleUploadedFile("test_file.jpg", file_data)
        response = self.client.post("/v1/file", {"myProfilePic" : dummy_file})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for post request for /v1/file endpoint
    @patch("boto3.client")
    def test_post_file_without_user_id(self, mock_obj):
        # Creating dummy file to upload
        file_data = b"abcdef"
        file_name = "test_file.jpg"
        dummy_file = SimpleUploadedFile(file_name, file_data)
        # Setting upload date
        upload_date = datetime.now().date().strftime("%Y-%m-%d")
        # Sending request
        response = self.client.post("/v1/file", {"profilePic" : dummy_file})
        # Checking for status code and headers
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Cache-Control" in response.headers)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        # Converting response to json and creating similar mock
        json_response = json.loads(response.content.decode("utf-8"))
        user_id = json_response["id"]
        # Setting url
        url = f"{config('BUCKET_NAME')}/{user_id}/{file_name}"
        response_data = {
            "file_name" : file_name,
            "id" : user_id,
            "url" : url,
            "upload_date" : upload_date
        }
        self.assertEqual(response_data, json_response)
    
    # Testcase for head request for /v1/file/user_id endpoint
    def test_head_file_with_user_id(self):
        response = self.client.head("/v1/file/123abc-cde")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for options request for /v1/file/user_id endpoint
    def test_options_file_with_user_id(self):
        response = self.client.options("/v1/file/123abc-cde")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for patch request for /v1/file/user_id endpoint
    def test_patch_file_with_user_id(self):
        response = self.client.patch("/v1/file/123abc-cde")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for put request for /v1/file/user_id endpoint
    def test_put_file_with_user_id(self):
        response = self.client.put("/v1/file/123abc-cde")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for post request for /v1/file/user_id endpoint
    def test_post_file_with_user_id(self):
        response = self.client.post("/v1/file/123abc-cde")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for get request for /v1/file/user_id endpoint where user id does not exist
    def test_get_file_with_user_id_not_exist(self):
        response = self.client.get("/v1/file/123abc-cde")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for get request for /v1/file/user_id endpoint where user id exist
    def test_get_file_with_user_id_exist(self):
        # Adding user entry in database so that it exists
        user_id = "123abc-cde"
        file_name = "abc.jpg"
        url = "123"
        upload_date = datetime.now().date()
        user_data_obj = UserData(user_id=user_id, file_name=file_name, url=url, upload_date=upload_date)
        user_data_obj.save()
        # Hitting api and getting response
        response = self.client.get(f"/v1/file/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Cache-Control" in response.headers)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        # Converting response to json and creating similar mock
        json_response = json.loads(response.content.decode("utf-8"))
        response_data = {
            "file_name" : file_name,
            "id" : user_id,
            "url" : url,
            "upload_date" : upload_date.strftime("%Y-%m-%d")
        }
        self.assertEqual(response_data, json_response)
    
    # Testcase for delete request for /v1/file/user_id endpoint where user id doesnt exist
    @patch("boto3.client")
    def test_delete_file_with_user_id_does_not_exist(self, mock_obj):
        response = self.client.delete(f"/v1/file/123abc-cde")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("Cache-Control" in response.headers)
    
    # Testcase for delete request for /v1/file/user_id endpoint where user id exist
    @patch("boto3.client")
    def test_delete_file_with_user_id_exist(self, mock_obj):
        # Adding user entry in database so that it exists
        user_id = "123abc-cde"
        file_name = "abc.jpg"
        url = "123"
        upload_date = datetime.now().date()
        user_data_obj = UserData(user_id=user_id, file_name=file_name, url=url, upload_date=upload_date)
        user_data_obj.save()
        # Hitting api and getting response
        response = self.client.delete(f"/v1/file/{user_id}")
        self.assertEqual(response.status_code, 204)
        self.assertTrue("Cache-Control" in response.headers)