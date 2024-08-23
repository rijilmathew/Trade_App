# tradeone/management/commands/setup_periodic_tasks.py
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from tradeone.periodic_tasks import setup_periodic_tasks

class Command(BaseCommand):
    help = 'Setup periodic tasks'

    def handle(self, *args, **options):
        setup_periodic_tasks()
        self.stdout.write(self.style.SUCCESS('Successfully set up periodic tasks'))
