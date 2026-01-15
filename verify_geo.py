import os
import django
from django.test import RequestFactory
from django.http import HttpResponse
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')
django.setup()

from ip_tracking.middleware import RequestLoggingMiddleware
from ip_tracking.models import RequestLog

def get_response(request):
    return HttpResponse("OK")

def verify():
    factory = RequestFactory()
    # Use a known public IP (e.g., Google DNS) to ensure geolocation works
    test_ip = '105.113.63.112' 
    
    print(f"Testing geolocation for IP: {test_ip}")
    
    request = factory.get('/')
    request.META['REMOTE_ADDR'] = test_ip
    
    middleware = RequestLoggingMiddleware(get_response)
    middleware(request)
    
    # Check the latest log
    log = RequestLog.objects.filter(ip_address=test_ip).last()
    
    if log and log.country:
        print(f"SUCCESS: Logged location: {log.city}, {log.country}")
    else:
        print("FAILURE: Geolocation data missing.")
        if log:
            print(f"Log found but empty location. Country: {log.country}, City: {log.city}")
        else:
            print("No log found.")

if __name__ == '__main__':
    verify()
