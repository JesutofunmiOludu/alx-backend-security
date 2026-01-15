import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def verify():
    client = Client()
    
    # 1. Test Anonymous (Limit: 5/m)
    print("\n--- Testing Anonymous Rate Limit (Should allow 5, block 6th) ---")
    for i in range(1, 8):
        response = client.get('/login/')
        status = response.status_code
        print(f"Request {i}: Status {status}")
        if status == 403:
            print("SUCCESS: Anonymous request blocked as expected.")
            break
            
    # Clean up potentially created block (django-ratelimit uses cache, flush it for next test if needed)
    from django.core.cache import cache
    cache.clear()
            
    # 2. Test Authenticated (Limit: 10/m)
    print("\n--- Testing Authenticated Rate Limit (Should allow 10, block 11th) ---")
    # Create test user
    user, created = User.objects.get_or_create(username='testuser')
    user.set_password('password')
    user.save()
    
    client.force_login(user)
    
    for i in range(1, 13):
        response = client.get('/login/')
        status = response.status_code
        print(f"Request {i}: Status {status}")
        if status == 403:
            print("SUCCESS: Authenticated request blocked as expected.")
            break

if __name__ == '__main__':
    verify()
