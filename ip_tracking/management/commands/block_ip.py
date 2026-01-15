from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Blocks a specific IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')
        parser.add_argument('--reason', type=str, help='Reason for blocking', default='')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f'IP {ip_address} is already blocked.'))
        else:
            BlockedIP.objects.create(ip_address=ip_address, reason=reason)
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP {ip_address}'))
