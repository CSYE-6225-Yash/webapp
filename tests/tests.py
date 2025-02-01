from django.test import TestCase
from unittest.mock import patch
from django.db.utils import OperationalError

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