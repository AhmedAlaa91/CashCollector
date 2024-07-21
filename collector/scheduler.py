import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.core.management import call_command

logger = logging.getLogger(__name__)

def my_job():
    logger.info("Running my job")
    call_command('my_command')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Run the job every 10 seconds
    scheduler.add_job(
        my_job,  # Pass the function directly
        trigger='interval',
         hours=1,
        id="my_job_id",
        replace_existing=True,
    )

    register_events(scheduler)
    scheduler.start()
    logger.info("Scheduler started")