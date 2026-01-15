import os
import django
import inspect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')
django.setup()

try:
    from django_ip_geolocation import utils
    print("Utils functions:")
    for name, obj in inspect.getmembers(utils):
        if inspect.isfunction(obj):
            print(f"- {name}")
            
    from django_ip_geolocation import middleware
    print("\nMiddleware classes:")
    for name, obj in inspect.getmembers(middleware):
        if inspect.isclass(obj):
            print(f"- {name}")
except ImportError as e:
    print(f"Error: {e}")
