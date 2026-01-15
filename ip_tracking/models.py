from django.db import models

# Create your models here.
class RequestLog(models.Model):
    ip_address = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    
    
