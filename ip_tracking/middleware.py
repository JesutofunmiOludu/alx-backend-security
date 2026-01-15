from ip_tracking.models import RequestLog, BlockedIP
import logging
from django.http import HttpResponseForbidden
import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access Denied: Your IP is blocked.")

        # Geolocation Fetching
        cache_key = f"ip_location_{ip_address}"
        location_data = cache.get(cache_key)

        if not location_data:
            try:
                response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    location_data = {
                        'country': data.get('country'),
                        'city': data.get('city')
                    }
                    cache.set(cache_key, location_data, 86400) # Cache for 24 hours
            except requests.RequestException:
                logger.error(f"Failed to fetch geolocation for {ip_address}")
                location_data = {}
        
        country = location_data.get('country') if location_data else None
        city = location_data.get('city') if location_data else None

        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
            country=country,
            city=city
        )
        
        response = self.get_response(request)
        return response

