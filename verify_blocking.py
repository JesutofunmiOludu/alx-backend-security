import os
import django
from django.test import RequestFactory
from django.http import HttpResponse, HttpResponseForbidden
from django.core.management import call_command
from io import StringIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')
django.setup()

from ip_tracking.middleware import RequestLoggingMiddleware
from ip_tracking.models import BlockedIP

def get_response(request):
    return HttpResponse("OK")

def verify():
    factory = RequestFactory()
    middleware = RequestLoggingMiddleware(get_response)
    ip_to_block = '10.0.0.1'
    
    # 1. Clean up
    BlockedIP.objects.filter(ip_address=ip_to_block).delete()
    
    # 2. Verify allowed
    print(f"Testing access for {ip_to_block} (should be allowed)...")
    request = factory.get('/')
    request.META['REMOTE_ADDR'] = ip_to_block
    resp = middleware(request)
    if resp.status_code == 200:
        print("SUCCESS: Access allowed.")
    else:
        print(f"FAILURE: Access denied (status {resp.status_code}).")
        return

    # 3. Block IP
    print(f"Blocking {ip_to_block}...")
    out = StringIO()
    call_command('block_ip', ip_to_block, stdout=out)
    print(out.getvalue().strip())
    
    # 4. Verify blocked
    print(f"Testing access for {ip_to_block} (should be blocked)...")
    request = factory.get('/')
    request.META['REMOTE_ADDR'] = ip_to_block
    resp = middleware(request)
    
    if resp.status_code == 403:
        print("SUCCESS: Access denied (403 Forbidden).")
    else:
        print(f"FAILURE: Access allowed (status {resp.status_code}).")

if __name__ == '__main__':
    verify()
