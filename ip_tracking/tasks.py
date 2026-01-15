from celery import shared_task
from django.utils import timezone
from .models import RequestLog, SuspiciousIP
from django.db.models import Count, Q

@shared_task
def flag_suspicious_ips():
    now = timezone.now()
    one_hour_ago = now - timezone.timedelta(hours=1)
    
    # 1. High Traffic Check: > 100 requests in last hour
    logs_last_hour = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    
    traffic_stats = logs_last_hour.values('ip_address').annotate(count=Count('id'))
    
    for stat in traffic_stats:
        ip = stat['ip_address']
        count = stat['count']
        
        if count > 100:
            if not SuspiciousIP.objects.filter(ip_address=ip, reason__contains='High traffic').exists():
                SuspiciousIP.objects.create(
                    ip_address=ip,
                    reason=f"High traffic: {count} requests in last hour"
                )

    # 2. Sensitive Path check
    # We'll check for requests to /admin or /login
    # A single access is probably fine for /login, but /admin might be suspicious if not authorized?
    # Prompt says: "flag IPs exceeding 100 requests/hour or accessing sensitive paths"
    # I will be strict for /admin if it's the raw login page, but maybe just flag "Sensitive Access".
    # To be practical, let's flag if they hit these paths.
    
    sensitive_logs = logs_last_hour.filter(Q(path__startswith='/admin') | Q(path__startswith='/login'))
    
    for log in sensitive_logs:
        ip = log.ip_address
        # Avoid duplicate flagging for same reason in reasonable time? 
        # Or just flag once.
        if not SuspiciousIP.objects.filter(ip_address=ip, reason__contains='Sensitive path').exists():
             SuspiciousIP.objects.create(
                ip_address=ip,
                reason=f"Sensitive path access: {log.path}"
            )
