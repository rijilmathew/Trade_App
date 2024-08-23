from django_celery_beat.models import CrontabSchedule, PeriodicTask
import logging
logger = logging.getLogger(__name__)
def setup_periodic_tasks():
    logger.info("Setting up periodic tasks...")
    # Create or get the schedule
    schedule_all_tasks, _ = CrontabSchedule.objects.get_or_create(
        minute='*',  # Every minute
        hour='9-15',  # From 9 AM to 3 PM
        day_of_week='1-5',  # Monday to Friday
    )

    # Create or update the periodic task
    PeriodicTask.objects.get_or_create(
        crontab=schedule_all_tasks,
        name='Run all tasks every minute from 9:00 AM to 3:00 PM (Monday to Friday)',
        task='tradeone.tasks.run_all_tasks',
        args='[]',
        kwargs='{}'
    )
