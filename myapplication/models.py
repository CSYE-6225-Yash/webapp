from django.db import models

class HealthCheck(models.Model):
    check_id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.check_id} - {self.date_time}"