from django.apps import AppConfig

import threading
class CollectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collector'


    def ready(self):
        import collector.scheduler
        collector.scheduler.start()
