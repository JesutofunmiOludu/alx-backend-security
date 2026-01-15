import os
import django
from django.test import RequestFactory
from django.http import HttpResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')
django.setup()

from ip_tracking.middleware import RequestLoggingMiddleware
from ip_tracking.models import RequestLog

def get_response(request):
    return HttpResponse("OK")

def verify():
    factory = RequestFactory()
    request = factory.get('/')
    request.META['REMOTE_ADDR'] = '1.2.3.4'
    
    middleware = RequestLoggingMiddleware(get_response)
    resp = middleware(request)
    
    print(f"Response status: {resp.status_code}")
    
    log_exists = RequestLog.objects.filter(ip_address='1.2.3.4', path='/').exists()
    if log_exists:
        print("SUCCESS: Log entry created.")
    else:
        print("FAILURE: No log entry found.")

if __name__ == '__main__':
    verify()
