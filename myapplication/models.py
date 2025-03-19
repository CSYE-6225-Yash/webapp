from django.db import models

class HealthCheck(models.Model):
    check_id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.check_id} - {self.date_time}"

class UserData(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    file_name = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)
    upload_date = models.DateField()
    obj_metadata = models.JSONField(null=True)

    def __str__(self):
        return f"{self.user_id} - {self.file_name}"