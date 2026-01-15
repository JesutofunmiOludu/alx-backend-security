from django.db import models

# Create your models here.
class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address}  | {self.path} | {self.timestamp}"
    
    
class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, unique=True, db_index=True)
    reason = models.TextField(blank=True, null=True)
    blocked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return f"{self.ip_address} - {self.blocked_at}" 