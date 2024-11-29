from django.db import models
from django.utils import timezone

# Create your models here.


class LoginAttempt(models.Model):
    username = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} - {self.ip_address} - {self.timestamp}"