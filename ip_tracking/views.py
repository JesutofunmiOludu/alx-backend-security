from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=False)
@ratelimit(key='ip', rate='10/m', block=False)
def login_view(request):
    # Check limits manually to differentiate messages if needed, 
    # but simplest is to check request.ratelimit which is set by the decorator.
    
    # Logic: 
    # If user is authenticated -> check 10/m limit
    # If user is anonymous -> check 5/m limit
    
    # Ideally, we separate keys.
    # Anonymous: key='ip', rate='5/m'
    # Authenticated: key='user', rate='10/m'
    
    # However, for a single login view, usually it's anonymous users trying to log in.
    # If they are already authenticated, they don't need to log in.
    # But the instructions say: "10 requests/minute (authenticated), 5 requests/minute (anonymous)"
    # This implies the view might be accessed by both? Or maybe it refers to API endpoints?
    # I will implement a robust check.
    
    # Note: django-ratelimit doesn't support conditional rates in one line easily without a callable.
    # I'll use a callable for rate or just two different checks.
    
    was_limited = False
    
    if request.user.is_authenticated:
        # Check 10/m for user
        limit_auth = ratelimit(key='user', rate='10/m', method='GET', block=True)
        # The decorator above on the function handles it if block=True, 
        # but here I am writing the body.
        # Actually, let's use the decorator properly.
        pass
    else:
        # Check 5/m for ip
        pass

    return HttpResponse("Login Page")

# Let's retry with a cleaner approach using the decorator properly
# We need a wrapper to decide which limit to apply?
# Or stacks of decorators.

# If we stack them:
# @ratelimit(key='ip', rate='5/m', block=True) -> This blocks everyone at 5/m per IP.
# If an authenticated user comes from same IP, they effectively get 5/m too if we blindly use IP.
# We want 10/m for authenticated users.

def custom_rate(group, request):
    if request.user.is_authenticated:
        return '10/m'
    return '5/m'
    
def custom_key(group, request):
    if request.user.is_authenticated:
        return request.user.username
    return request.META['REMOTE_ADDR'] # or 'ip' shorthand

@ratelimit(key=custom_key, rate=custom_rate, block=True)
def login_view(request):
    return HttpResponse("Login View - Access Granted")
