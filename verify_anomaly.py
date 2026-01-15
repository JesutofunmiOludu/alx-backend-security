import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')
django.setup()

from ip_tracking.models import RequestLog, SuspiciousIP
from ip_tracking.tasks import flag_suspicious_ips

def verify():
    print("Cleaning up...")
    RequestLog.objects.all().delete()
    SuspiciousIP.objects.all().delete()
    
    # 1. Test High Traffic (101 requests)
    ip_high = '1.1.1.1'
    print(f"Generating 101 requests for {ip_high}...")
    logs = [
        RequestLog(ip_address=ip_high, path='/home') 
        for _ in range(101)
    ]
    RequestLog.objects.bulk_create(logs)
    
    # 2. Test Sensitive Path
    ip_sensitive = '2.2.2.2'
    print(f"Generating sensitive access for {ip_sensitive}...")
    RequestLog.objects.create(ip_address=ip_sensitive, path='/admin/login')
    
    # Run task (synchronously)
    print("Running anomaly detection task...")
    flag_suspicious_ips()
    
    # Check results
    flagged_ips = SuspiciousIP.objects.all()
    print(f"\nFound {flagged_ips.count()} suspicious IPs.")
    
    for sip in flagged_ips:
        print(f"- {sip.ip_address}: {sip.reason}")
        
    expected_ips = {ip_high, ip_sensitive}
    found_ips = {sip.ip_address for sip in flagged_ips}
    
    if expected_ips.issubset(found_ips):
        print("\nSUCCESS: Both IPs flagged correctly.")
    else:
        print(f"\nFAILURE: Expected {expected_ips}, found {found_ips}")

if __name__ == '__main__':
    verify()
